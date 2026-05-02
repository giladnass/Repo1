'use strict';

/*
 * TaskOS — Obsidian plugin
 * MVP: Phase 0 + Phase 1 (vault scaffold + plugin views, no AI yet)
 *
 * Source of truth: Markdown files under <rootFolder>/Tasks/, /Projects/, etc.
 * This plugin reads and writes those files. It does not own a separate database.
 */

const obsidian = require('obsidian');
const {
  Plugin,
  ItemView,
  Modal,
  Notice,
  Setting,
  PluginSettingTab,
  parseYaml,
  stringifyYaml,
} = obsidian;

const VIEW_TYPE_TASKOS = 'taskos-view';

const DEFAULT_SETTINGS = {
  rootFolder: 'TaskOS',
};

// status -> folder under <root>/Tasks/
// "scheduled" lives in Active because it's still actionable.
// "canceled" lives in Completed because it's archival.
const STATUS_FOLDERS = {
  inbox: 'Tasks/Inbox',
  active: 'Tasks/Active',
  scheduled: 'Tasks/Active',
  waiting: 'Tasks/Waiting',
  someday: 'Tasks/Someday',
  completed: 'Tasks/Completed',
  canceled: 'Tasks/Completed',
};

const STATUS_OPTIONS = ['inbox', 'active', 'scheduled', 'waiting', 'someday', 'completed', 'canceled'];
const PRIORITY_OPTIONS = ['', 'low', 'medium', 'high', 'critical'];

// ---------- helpers ----------

function pad(n) { return String(n).padStart(2, '0'); }

function newTaskId(date) {
  const d = date || new Date();
  const rand = Math.random().toString(36).slice(2, 6);
  return `task_${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}_${rand}`;
}

function isoNow() {
  const d = new Date();
  const tz = -d.getTimezoneOffset();
  const sign = tz >= 0 ? '+' : '-';
  const tzh = pad(Math.floor(Math.abs(tz) / 60));
  const tzm = pad(Math.abs(tz) % 60);
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}${sign}${tzh}:${tzm}`;
}

function todayStr() {
  const d = new Date();
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
}

function slugify(s) {
  return (s || 'untitled')
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 60) || 'untitled';
}

function stripWikiBrackets(s) {
  if (!s || typeof s !== 'string') return s;
  const m = s.match(/^\[\[(.+?)\]\]$/);
  return m ? m[1] : s;
}

function splitFrontmatter(content) {
  const m = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!m) return { frontmatter: null, body: content };
  try {
    const fm = parseYaml(m[1]) || {};
    return { frontmatter: fm, body: m[2] };
  } catch (e) {
    return { frontmatter: null, body: content, parseError: String(e && e.message || e) };
  }
}

function joinFrontmatter(fm, body) {
  const yaml = stringifyYaml(fm).replace(/\s+$/, '');
  const sep = body.startsWith('\n') ? '' : '\n';
  return `---\n${yaml}\n---\n${sep}${body}`;
}

function emptyTaskFrontmatter({ title, project, due, priority, tags, people, status }) {
  const id = newTaskId();
  const now = isoNow();
  return {
    id,
    type: 'task',
    title: title || '',
    status: status || 'inbox',
    priority: priority || null,
    due: due || null,
    scheduled: null,
    deferred_until: null,
    project: project || null,
    area: null,
    people: people || [],
    tags: tags || [],
    source: null,
    created: now,
    updated: now,
    completed: null,
    recurrence: null,
  };
}

// ---------- repository ----------

class TaskRepo {
  constructor(plugin) { this.plugin = plugin; }
  get vault() { return this.plugin.app.vault; }
  get root() { return this.plugin.settings.rootFolder; }

  async ensureFolder(path) {
    const existing = this.vault.getAbstractFileByPath(path);
    if (!existing) {
      try { await this.vault.createFolder(path); }
      catch (e) { /* may already exist due to race; ignore */ }
    }
  }

  async ensureFolders() {
    const folders = [
      this.root,
      `${this.root}/Tasks`,
      `${this.root}/Tasks/Inbox`,
      `${this.root}/Tasks/Active`,
      `${this.root}/Tasks/Waiting`,
      `${this.root}/Tasks/Someday`,
      `${this.root}/Tasks/Completed`,
      `${this.root}/Projects`,
      `${this.root}/Areas`,
      `${this.root}/People`,
      `${this.root}/Daily`,
      `${this.root}/Templates`,
      `${this.root}/.system`,
    ];
    for (const f of folders) await this.ensureFolder(f);
  }

  folderForStatus(status) {
    return `${this.root}/${STATUS_FOLDERS[status] || STATUS_FOLDERS.inbox}`;
  }

  fileNameFor(fm) {
    return `${slugify(fm.title)}__${fm.id}.md`;
  }

  taskBody(fm) {
    const stamp = fm.created.slice(0, 16).replace('T', ' ');
    return `\n# ${fm.title}\n\n## Notes\n\n## Activity Log\n- ${stamp} — Created\n`;
  }

  async create(fm) {
    await this.ensureFolders();
    const folder = this.folderForStatus(fm.status);
    const path = `${folder}/${this.fileNameFor(fm)}`;
    const content = joinFrontmatter(fm, this.taskBody(fm));
    return await this.vault.create(path, content);
  }

  isTaskFile(file) {
    return file && file.extension === 'md' && file.path.startsWith(`${this.root}/Tasks/`);
  }

  allTaskFiles() {
    return this.vault.getFiles().filter(f => this.isTaskFile(f));
  }

  allProjectFiles() {
    const folder = `${this.root}/Projects/`;
    return this.vault.getFiles().filter(f => f.extension === 'md' && f.path.startsWith(folder));
  }

  async readTask(file) {
    try {
      const raw = await this.vault.read(file);
      const { frontmatter, body, parseError } = splitFrontmatter(raw);
      if (!frontmatter || frontmatter.type !== 'task') return null;
      return { file, fm: frontmatter, body, parseError };
    } catch (e) {
      console.error('TaskOS: failed to read', file && file.path, e);
      return null;
    }
  }

  async readAllTasks() {
    const files = this.allTaskFiles();
    const tasks = [];
    for (const f of files) {
      const t = await this.readTask(f);
      if (t) tasks.push(t);
    }
    return tasks;
  }

  async update(task, patch) {
    const oldStatus = task.fm.status;
    const newFm = Object.assign({}, task.fm, patch, { updated: isoNow() });
    const newStatus = newFm.status;

    let file = task.file;
    if (oldStatus !== newStatus) {
      const targetFolder = this.folderForStatus(newStatus);
      await this.ensureFolder(targetFolder);
      const newPath = `${targetFolder}/${file.name}`;
      if (file.path !== newPath) {
        await this.vault.rename(file, newPath);
        const moved = this.vault.getAbstractFileByPath(newPath);
        if (moved) file = moved;
      }
    }
    const content = joinFrontmatter(newFm, task.body);
    await this.vault.modify(file, content);
    return { file, fm: newFm, body: task.body };
  }

  async complete(task) {
    const now = isoNow();
    return await this.update(task, { status: 'completed', completed: now });
  }

  async reopen(task) {
    return await this.update(task, { status: 'active', completed: null });
  }

  // Move misplaced files so folder matches status. Status field is canonical.
  async reconcile() {
    const tasks = await this.readAllTasks();
    let moved = 0;
    for (const t of tasks) {
      const target = this.folderForStatus(t.fm.status);
      const targetPath = `${target}/${t.file.name}`;
      if (t.file.path !== targetPath) {
        await this.ensureFolder(target);
        try {
          await this.vault.rename(t.file, targetPath);
          moved++;
        } catch (e) { console.error('TaskOS reconcile rename failed', t.file.path, e); }
      }
    }
    return { moved, total: tasks.length };
  }
}

// ---------- Quick capture modal ----------

class QuickCaptureModal extends Modal {
  constructor(plugin) { super(plugin.app); this.plugin = plugin; }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass('taskos-modal');
    contentEl.createEl('h2', { text: 'Quick capture' });

    this.state = { title: '', due: '', project: '', priority: '', tags: '' };

    const titleSetting = new Setting(contentEl).setName('Title').setDesc('What needs doing?');
    titleSetting.addText(t => {
      t.setPlaceholder('e.g. Follow up with Dani about the cybersecurity deck');
      t.onChange(v => this.state.title = v);
      window.setTimeout(() => t.inputEl.focus(), 30);
      t.inputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.submit(); }
      });
    });

    new Setting(contentEl).setName('Due date').setDesc('YYYY-MM-DD (optional)')
      .addText(t => t.setPlaceholder('2026-05-10').onChange(v => this.state.due = v));

    new Setting(contentEl).setName('Project').setDesc('Optional. Will be linked as [[Project Name]].')
      .addText(t => {
        t.setPlaceholder('e.g. Cybersecurity GTM');
        t.onChange(v => this.state.project = v);
        // datalist of existing projects
        const dlId = 'taskos-projects-' + Math.random().toString(36).slice(2, 6);
        const dl = t.inputEl.parentElement.createEl('datalist', { attr: { id: dlId } });
        for (const p of this.plugin.repo.allProjectFiles()) {
          dl.createEl('option', { value: p.basename });
        }
        t.inputEl.setAttr('list', dlId);
      });

    new Setting(contentEl).setName('Priority')
      .addDropdown(d => {
        for (const p of PRIORITY_OPTIONS) d.addOption(p, p || '—');
        d.onChange(v => this.state.priority = v);
      });

    new Setting(contentEl).setName('Tags').setDesc('Comma-separated (optional)')
      .addText(t => t.setPlaceholder('positioning, follow-up').onChange(v => this.state.tags = v));

    const btns = contentEl.createDiv({ cls: 'taskos-modal-buttons' });
    const cancel = btns.createEl('button', { text: 'Cancel' });
    cancel.onclick = () => this.close();
    const ok = btns.createEl('button', { text: 'Capture', cls: 'mod-cta' });
    ok.onclick = () => this.submit();
  }

  async submit() {
    const { title, due, project, priority, tags } = this.state;
    if (!title || !title.trim()) { new Notice('TaskOS: title is required'); return; }
    if (due && !/^\d{4}-\d{2}-\d{2}$/.test(due.trim())) {
      new Notice('TaskOS: due date must be YYYY-MM-DD'); return;
    }
    const tagList = (tags || '').split(',').map(s => s.trim()).filter(Boolean);
    const projectVal = project && project.trim() ? `[[${project.trim()}]]` : null;
    const fm = emptyTaskFrontmatter({
      title: title.trim(),
      due: due ? due.trim() : null,
      project: projectVal,
      priority: priority || null,
      tags: tagList,
    });
    try {
      await this.plugin.repo.create(fm);
      new Notice(`TaskOS: captured "${fm.title}"`);
      this.close();
      this.plugin.refreshView();
    } catch (e) {
      console.error('TaskOS capture failed', e);
      new Notice('TaskOS: capture failed — see console');
    }
  }

  onClose() { this.contentEl.empty(); }
}

// ---------- Side panel view ----------

const FILTERS = [
  { id: 'today', label: 'Today' },
  { id: 'inbox', label: 'Inbox' },
  { id: 'upcoming', label: 'Upcoming' },
  { id: 'overdue', label: 'Overdue' },
  { id: 'waiting', label: 'Waiting' },
  { id: 'someday', label: 'Someday' },
  { id: 'project', label: 'By project' },
  { id: 'completed', label: 'Completed' },
];

class TaskOSView extends ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.activeFilter = 'today';
    this.activeProject = null;
  }

  getViewType() { return VIEW_TYPE_TASKOS; }
  getDisplayText() { return 'TaskOS'; }
  getIcon() { return 'check-circle'; }

  async onOpen() {
    this.contentEl.addClass('taskos-view');
    await this.render();
  }
  async onClose() {}

  async render() {
    const tasks = await this.plugin.repo.readAllTasks();
    this.contentEl.empty();

    // Header
    const header = this.contentEl.createDiv({ cls: 'taskos-header' });
    header.createEl('h3', { text: 'TaskOS', cls: 'taskos-title-h' });
    const right = header.createDiv({ cls: 'taskos-header-right' });
    const captureBtn = right.createEl('button', { text: '+ Capture', cls: 'mod-cta' });
    captureBtn.onclick = () => new QuickCaptureModal(this.plugin).open();
    const refreshBtn = right.createEl('button', { text: '↻' });
    refreshBtn.setAttr('title', 'Refresh');
    refreshBtn.onclick = () => this.render();

    // Filter tabs
    const tabs = this.contentEl.createDiv({ cls: 'taskos-tabs' });
    for (const f of FILTERS) {
      const cls = 'taskos-tab' + (this.activeFilter === f.id ? ' active' : '');
      const btn = tabs.createEl('button', { text: f.label, cls });
      btn.onclick = () => {
        this.activeFilter = f.id;
        if (f.id !== 'project') this.activeProject = null;
        this.render();
      };
    }

    // Project picker if needed
    if (this.activeFilter === 'project') {
      const projects = this.plugin.repo.allProjectFiles().map(f => f.basename).sort();
      const picker = this.contentEl.createDiv({ cls: 'taskos-project-picker' });
      picker.createEl('label', { text: 'Project: ' });
      const sel = picker.createEl('select');
      sel.createEl('option', { value: '', text: '— pick a project —' });
      for (const p of projects) {
        const opt = sel.createEl('option', { value: p, text: p });
        if (p === this.activeProject) opt.selected = true;
      }
      sel.onchange = () => { this.activeProject = sel.value || null; this.render(); };
    }

    // Filter + render list
    const filtered = this.applyFilter(tasks, this.activeFilter, this.activeProject);
    const meta = this.contentEl.createDiv({ cls: 'taskos-meta' });
    meta.setText(`${filtered.length} task${filtered.length === 1 ? '' : 's'}`);

    const list = this.contentEl.createDiv({ cls: 'taskos-list' });
    if (filtered.length === 0) {
      list.createDiv({ cls: 'taskos-empty', text: 'Nothing here.' });
    }
    for (const t of filtered) this.renderTask(list, t);

    // Footer
    const footer = this.contentEl.createDiv({ cls: 'taskos-footer' });
    const reconcile = footer.createEl('button', { text: 'Reconcile folders' });
    reconcile.setAttr('title', 'Move files so folder matches status field. Status is the source of truth.');
    reconcile.onclick = async () => {
      const r = await this.plugin.repo.reconcile();
      new Notice(`TaskOS: moved ${r.moved} of ${r.total} task files`);
      this.render();
    };
    const ensure = footer.createEl('button', { text: 'Ensure folders' });
    ensure.setAttr('title', 'Create any missing TaskOS folders');
    ensure.onclick = async () => {
      await this.plugin.repo.ensureFolders();
      new Notice('TaskOS: folders ensured');
      this.render();
    };
  }

  applyFilter(tasks, filter, projectName) {
    const today = todayStr();
    const sortByDueThenCreated = (a, b) => {
      const da = a.fm.due || '9999-12-31';
      const db = b.fm.due || '9999-12-31';
      if (da !== db) return da < db ? -1 : 1;
      const ca = a.fm.created || '';
      const cb = b.fm.created || '';
      return ca.localeCompare(cb);
    };
    const open = tasks.filter(t => !['completed', 'canceled'].includes(t.fm.status));

    switch (filter) {
      case 'today':
        return open.filter(t => {
          const due = t.fm.due;
          const sched = t.fm.scheduled;
          if (sched && sched <= today) return true;
          if (due && due <= today) return true;
          return false;
        }).sort(sortByDueThenCreated);
      case 'inbox':
        return tasks.filter(t => t.fm.status === 'inbox').sort(sortByDueThenCreated);
      case 'upcoming':
        return open.filter(t => t.fm.due && t.fm.due > today).sort(sortByDueThenCreated);
      case 'overdue':
        return open.filter(t => t.fm.due && t.fm.due < today).sort(sortByDueThenCreated);
      case 'waiting':
        return tasks.filter(t => t.fm.status === 'waiting').sort(sortByDueThenCreated);
      case 'someday':
        return tasks.filter(t => t.fm.status === 'someday').sort(sortByDueThenCreated);
      case 'completed':
        return tasks.filter(t => t.fm.status === 'completed')
          .sort((a, b) => (b.fm.completed || '').localeCompare(a.fm.completed || ''));
      case 'project':
        if (!projectName) return [];
        return open.filter(t => stripWikiBrackets(t.fm.project) === projectName).sort(sortByDueThenCreated);
      default:
        return open.sort(sortByDueThenCreated);
    }
  }

  renderTask(parent, t) {
    const row = parent.createDiv({ cls: 'taskos-row' });

    const cb = row.createEl('input', { type: 'checkbox' });
    cb.checked = t.fm.status === 'completed';
    cb.onclick = async (e) => {
      e.stopPropagation();
      try {
        if (cb.checked) await this.plugin.repo.complete(t);
        else await this.plugin.repo.reopen(t);
      } catch (err) {
        console.error('TaskOS toggle failed', err);
        new Notice('TaskOS: update failed');
      }
      this.render();
    };

    const main = row.createDiv({ cls: 'taskos-main' });
    const titleEl = main.createDiv({ cls: 'taskos-title' });
    titleEl.setText(t.fm.title || t.file.basename);
    if (t.fm.status === 'completed') titleEl.addClass('completed');

    const sub = main.createDiv({ cls: 'taskos-sub' });
    const today = todayStr();
    if (t.fm.due) {
      const span = sub.createSpan({ cls: 'taskos-due' });
      if (t.fm.due < today && t.fm.status !== 'completed') {
        span.addClass('overdue');
        span.setText(`overdue ${t.fm.due}`);
      } else {
        span.setText(`due ${t.fm.due}`);
      }
    }
    if (t.fm.priority) {
      sub.createSpan({ cls: `taskos-priority pri-${t.fm.priority}`, text: t.fm.priority });
    }
    const projectName = stripWikiBrackets(t.fm.project);
    if (projectName) {
      sub.createSpan({ cls: 'taskos-project', text: projectName });
    }
    if (t.fm.status && !['inbox', 'active', 'completed'].includes(t.fm.status)) {
      sub.createSpan({ cls: 'taskos-status', text: t.fm.status });
    }
    if (Array.isArray(t.fm.tags) && t.fm.tags.length) {
      for (const tag of t.fm.tags.slice(0, 3)) {
        sub.createSpan({ cls: 'taskos-tag', text: '#' + tag });
      }
    }
    if (t.parseError) {
      sub.createSpan({ cls: 'taskos-error', text: 'YAML parse error' });
    }

    main.onclick = () => {
      this.app.workspace.getLeaf(false).openFile(t.file);
    };
  }
}

// ---------- Settings tab ----------

class TaskOSSettingTab extends PluginSettingTab {
  constructor(app, plugin) { super(app, plugin); this.plugin = plugin; }

  display() {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.createEl('h2', { text: 'TaskOS' });

    new Setting(containerEl)
      .setName('Root folder')
      .setDesc('Folder inside this vault where TaskOS reads/writes its files. Default: TaskOS')
      .addText(t => t
        .setValue(this.plugin.settings.rootFolder)
        .onChange(async v => {
          const next = (v || 'TaskOS').trim().replace(/\/+$/, '') || 'TaskOS';
          this.plugin.settings.rootFolder = next;
          await this.plugin.saveSettings();
        }));

    containerEl.createEl('h3', { text: 'Data' });
    const dataDesc = containerEl.createEl('p');
    dataDesc.innerHTML = `Tasks are individual Markdown files under <code>${this.plugin.settings.rootFolder}/Tasks/</code>. Projects under <code>${this.plugin.settings.rootFolder}/Projects/</code>. You can open, edit, search, and version-control these files with any tool. The plugin holds no separate database.`;

    containerEl.createEl('h3', { text: 'AI providers' });
    const aiDesc = containerEl.createEl('p');
    aiDesc.setText('AI features are not enabled in this build. The data layer is shaped to support a model-agnostic provider (Anthropic, OpenAI, Gemini, local) in a later phase. The Markdown remains canonical regardless.');

    containerEl.createEl('h3', { text: 'Commands' });
    const cmds = containerEl.createEl('ul');
    cmds.createEl('li', { text: 'Open TaskOS panel — open the side view' });
    cmds.createEl('li', { text: 'Quick capture task — Cmd/Ctrl+Shift+T' });
    cmds.createEl('li', { text: 'Reconcile folders to status — fix any folder/status mismatches' });
    cmds.createEl('li', { text: 'Create TaskOS folder structure — set up missing folders' });
  }
}

// ---------- Main plugin ----------

module.exports = class TaskOSPlugin extends Plugin {
  async onload() {
    await this.loadSettings();
    this.repo = new TaskRepo(this);

    this.registerView(VIEW_TYPE_TASKOS, (leaf) => new TaskOSView(leaf, this));

    this.addRibbonIcon('check-circle', 'Open TaskOS', () => this.activateView());

    this.addCommand({
      id: 'taskos-open-view',
      name: 'Open TaskOS panel',
      callback: () => this.activateView(),
    });
    this.addCommand({
      id: 'taskos-quick-capture',
      name: 'Quick capture task',
      hotkeys: [{ modifiers: ['Mod', 'Shift'], key: 'T' }],
      callback: () => new QuickCaptureModal(this).open(),
    });
    this.addCommand({
      id: 'taskos-reconcile',
      name: 'Reconcile folders to status',
      callback: async () => {
        const r = await this.repo.reconcile();
        new Notice(`TaskOS: moved ${r.moved} of ${r.total} task files`);
        this.refreshView();
      },
    });
    this.addCommand({
      id: 'taskos-ensure-folders',
      name: 'Create TaskOS folder structure',
      callback: async () => {
        await this.repo.ensureFolders();
        new Notice('TaskOS: folders ensured');
      },
    });

    this.addSettingTab(new TaskOSSettingTab(this.app, this));

    // Live refresh on vault changes inside our root folder
    const onAny = (file) => {
      if (!file || !file.path) return;
      if (!file.path.startsWith(`${this.settings.rootFolder}/`)) return;
      window.clearTimeout(this._refreshTimer);
      this._refreshTimer = window.setTimeout(() => this.refreshView(), 250);
    };
    this.registerEvent(this.app.vault.on('modify', onAny));
    this.registerEvent(this.app.vault.on('create', onAny));
    this.registerEvent(this.app.vault.on('delete', onAny));
    this.registerEvent(this.app.vault.on('rename', onAny));
  }

  refreshView() {
    const leaves = this.app.workspace.getLeavesOfType(VIEW_TYPE_TASKOS);
    for (const leaf of leaves) {
      if (leaf.view && typeof leaf.view.render === 'function') {
        leaf.view.render();
      }
    }
  }

  async activateView() {
    const existing = this.app.workspace.getLeavesOfType(VIEW_TYPE_TASKOS)[0];
    if (existing) {
      this.app.workspace.revealLeaf(existing);
      return;
    }
    let leaf = null;
    if (typeof this.app.workspace.getRightLeaf === 'function') {
      leaf = this.app.workspace.getRightLeaf(false);
    }
    if (!leaf) leaf = this.app.workspace.getLeaf(true);
    await leaf.setViewState({ type: VIEW_TYPE_TASKOS, active: true });
    this.app.workspace.revealLeaf(leaf);
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() { await this.saveData(this.settings); }

  onunload() {
    window.clearTimeout(this._refreshTimer);
  }
};
