---
title: "NotebookLM: Migrating Data Between Google Accounts via Takeout"
tags: [notebooklm, google-takeout, migration, tools, workflow]
created: 2026-04-15
updated: 2026-04-15
source: "[[notebooklm-google-takeout-migration-qa]]"
status: active
---

# NotebookLM: Migrating Data Between Google Accounts via Takeout

## Summary

There is **no native import feature** in NotebookLM. You cannot automatically restore a Google Takeout archive into a new account. Migration must be done manually, but it is achievable by following the steps below.

## What Google Takeout Exports from NotebookLM

When you download NotebookLM data via Google Takeout, the archive typically contains:

- Uploaded source files (PDFs, text files, etc.)
- Generated notes
- Chat history (in JSON format)
- Generated Audio Overviews

## Migration Steps

### 1. Extract the Takeout Archive

Unzip the downloaded file. The contents will be organized into folders per notebook.

### 2. Manually Recreate Notebooks

1. Log into NotebookLM with the new Google account.
2. Create a new notebook.
3. Re-upload source files (PDFs, text files) by dragging them in from the unzipped folder.
4. **For Google Docs/Drive sources**: Share the original files with the new Google account and import them directly from Drive — they cannot be exported and re-imported as files.

### 3. Preserve Notes and Chat History

Chat histories and notes do **not** auto-populate back into the NotebookLM interface. The workaround:

- Combine important chat logs, summaries, or generated notes into a single **Google Doc** or **Markdown (.md) file**.
- Upload that document as a source in the new notebook so the AI retains historical context.

### 4. Convert JSON Chat History (Optional)

If the chat history exported as a dense JSON file, community scripts can convert it to clean Markdown:

- Search GitHub for: `NotebookLM JSON to Markdown`
- These scripts automate the conversion, producing files that are easy to read and upload as sources.

## Key Limitations

| Item | Migrates? | Notes |
|---|---|---|
| Uploaded PDFs / text files | Yes | Drag and drop from Takeout folder |
| Google Docs / Drive sources | Partial | Must re-share with new account |
| Generated notes | Manual | Convert to doc/MD and upload as source |
| Chat history | Manual | Convert JSON → MD via community script, upload as source |
| Audio Overviews | No | Must regenerate in new account |

## Related Tools / Resources

- Google Takeout: [takeout.google.com](https://takeout.google.com)
- GitHub search: `NotebookLM JSON to Markdown` — community conversion scripts

## See Also

- [[NotebookLM]] (if/when a general NotebookLM page is created)
