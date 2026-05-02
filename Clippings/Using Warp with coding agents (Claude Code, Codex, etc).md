In summary, Warp's integration with coding agents like Claude Code and Codex offers a streamlined terminal experience with features such as a dedicated compose menu, voice-to-text input, and vertical tab management, enhancing productivity through customizable tab configurations, integrated code review panels, and Git worktree automation.

## Headlines

- **Warp enhances coding agent workflows:** It provides a dedicated compose menu, voice-to-text input, and vertical tab management for improved productivity.
- **Customization and integration are key:** Users can leverage custom tab configurations and integrated code review panels to optimize their terminal experience.
- **Automation streamlines processes:** Git worktree automation helps manage workflows efficiently while maintaining visibility into agent sessions.

## Things

- **People:** Ben Holmes
- **Places:** N/A
- **Numbers:** 10,377 views, 318 subscribers
- **Things:** Warp, coding agents, Claude Code, Codex, terminal, compose menu, voice-to-text, vertical tabs, code review panels, Git worktree
- **Concepts:** Productivity, workflow optimization, automation, integration, session management

---

![](https://www.youtube.com/watch?v=Fw4wBzmSX_8)

## Transcript

**0:00** · As a developer, your job is probably running a bunch of coding agents at the same time. And it's not really hard to prompt agents anymore. The hard part is managing all of the agents you have running simultaneously. Now, you might be a tmux warrior that can manage eight panes at once like a stock trader, but if you're like me, coming from IDEs or Visual Studio Code, you want something that just kind of manages it all for you. The Warp team's been thinking a lot about this, so I'm going to show you what we've cooked up to make it easier to work with a bunch of agents in your terminal.

**0:30** · Going to talk about voice input, code review, work trees, vertical tabs, and even choosing the default agent you want to run whenever you make a new tab. I'm going to start by explaining how to work with agents in a single session, and then we'll talk about multiple tabs of agents at the same time. So, to start up a coding agent, I'm just going to run Claude, and you get the same output you would expect. Uh but you also get a nice little toolbar at the bottom to work with this agent a little bit more easily.

**0:57** · So, right now I'm inside of this metric tricks project, and I want to add a skill for some of the scripts that I have inside of here. Now, I can start typing this out like create a skill.

**1:10** · Uh but once you start typing a little bit deeper, you may run into the common issues you have with TUIs. Like if I wanted to move my cursor to the start to fix a typo or add some details, I can't do that. I kind of have to arrow through with my keyboard in order to find that thing or use little jump shortcuts in order to get there. And for longer prompts, this gets really annoying really quickly. So, off the bat, I'm going to show you this nice little thing called a compose menu that Warp has built into it. So, if I hit compose, this gives you a separate box that you can type in that's a lot nicer to use.

**1:43** · It feels more like a regular ChatGPT-style box. So, if I wanted to say uh distill these scripts into a skill, it types like a normal input, but you can also move your cursor. Imagine that. And even crazier, you can add multi-cursor if you hold the command key. So, if you wanted to like make multi-line edits, that works just as well. So, you can be a power user, but you can also just be a regular old person. And we also have a voice input button.

**2:11** · This is really helpful if you're using agents that don't have voice input like OpenCode, CodeX, or most of the other CLIs really. So, if I wanted to speak out this whole prompt, I could do so. It's going to use Whisper Flo to transcribe it for me.

**2:24** · I want to distill all of the scripts that we've run into a reusable skill for the next time that we have a month of live streams to analyze.

**2:34** · You can also hold the function key in order to do that. You will notice when you're done, it'll paste it straight into the Claude Code box that you're ready to execute it and go back into the flow.

**2:44** · Now, let's add another agent to the party. So, if I wanted to add a new tab inside of here, I'm going to click on this tabs panel at the top. Now, I have vertical tabs enabled in my terminal.

**2:55** · You can also just use a regular horizontal tab bar if you want to, but if you use vertical mode, you can get some more metadata inside of here like whether an agent's running inside of this tab, the status of that agent, so you get blocked right here because it's waiting on my approval, and also a summary of the full conversation if you hover over that tab, which is really useful. So, see right away this thing is blocked and needs my approval. I'll hop in and say I allow reading skills from this project certainly, and then I'll just open a new tab with command T and go on to my next agent session.

**3:24** · Now, as you can imagine, you can stay on top of that other agent while it's running without losing track of it. And you can see if it's blocked in the future, you get an in-app notification for it. So, it's describing what it wants to do.

**3:37** · Here it wants to run a bash command. I can jump over, give it that approval, and then hop back to whatever I was doing. All right. So, I'm going to let that cook, and I'm going to hop over to another project that I want to work on.

**3:49** · And just for the sake of variety, I'm going to use a different coding agent like OpenCode for this one. Can use CodeX, Copilot, whatever you want to do.

**3:57** · And you notice here, now we're inside of our OpenCode session, and we get our same toolbelt that we got before. But now, because this is an active branch with some unstaged changes, we get this little callout for the code review panel. So, in here we can see the over/under on all the files that were changed. You also get that status at the top of the app. And clicking on it will give us a panel to view all of those changes in line, and I can of course resize this so you can see everything.

**4:24** · You also have a maximize button if you want to view it as a full-screen panel, and this will give you something that looks a lot like VS Code or GitHub Desktop or any other tool that you might have been using to manage all of the changes made by an agent, but now it's inside the terminal, but just a little bit more convenient. So, I'm going to collapse that sidebar there, and we can see we get a list of all the files that were changed with little hot buttons to go to each of those files. Uh you can also view all of the changes inside of here in one big scrolling list, which makes it easy to review large diffs.

**4:53** · You can also collapse them if you want to drill into specific tabs. It's almost like a PR review, really, where you can hop into everything that the agent did, you can view all of the changes, and you can interact with them as well to give an agent feedback on what it did. So, there's a paperclip up here if you want to attach a whole file as context and ask a question about it, but you also have an inline button if you want to specifically add comments on a line.

**5:19** · So, instead of jumping to GitHub and leaving a PR review, then maybe having an agent over there like Code Rabbit fix it for you, you don't have to do that. You can just do it with whatever agent's on your computer already. So, if I wanted to leave a comment here, for example, I could do that, and I could say, "Will this support And you can leave that comment in as many comments as you want. You have an overview here of everything that you've left it. And when you're ready to go, you can send it to your coding agent.

**5:51** · Here it says it's going to send to OpenCode since I already have that open inside of this tab. So, if I hit send agent, you'll notice that it plops it into my OpenCode box with a list of all of the changes that it needs to review.

**6:04** · Then I can send that off and have Big Pickle work on those fixes for me. Love it's called Big Pickle. And I can also check on that Claude Code task. We can see in the notifications panel, it's blocked again because Claude loves asking for permissions for everything.

**6:16** · Of course, it's a very safe model.

**6:19** · So, we're going to let it create that Claude skill, and actually might give it a bit of feedback here and say, "Put that skill in the current project repo."

**6:31** · \[snorts\] And then I can hop back over with control tab to the other thing that I'm working on, or I can open the tabs panel to conveniently go between the two, and we can see some nice logos and status symbols while each of these are working.

**6:44** · And now, because why not, I'm going to get a third agent going to show you what that's like, maybe working on my server repository. And to do that, I'm going to branch off with a work tree this time because you might be the type to say, "I want to have multiple agents working on the same repository at once. I don't want to clone that repo multiple times.

**7:03** · I also don't really want to learn Git work trees, to be honest. I just want a system that helps me set up a work tree so I can have a bunch of agents running at the same time." Well, Warp has something built in in order to do that.

**7:15** · If you click on the add button up here, you can see a full array of pre-built, we call tab configs to help you jump into a specific kind of session. And we're going to talk about tab configs in a second, but I'll point you to the work tree config. This is how you can set up all of your coding repositories so that you can quickly create a new work tree off of a repo that you want to track.

**7:37** · And I already have a few of them tracked inside of here. You have a button to add a new repo, by the way. And this just takes you to your project picker, as you can imagine. So, if I wanted to add this repo, for example, I can do that, and now I'm able to create work trees off of that repository. So, if I wanted to make a new work tree off of Warp Server, for example, I can click on that, and this will, right away, put me into that directory and create a new work tree off of that branch. And by default, we'll create it inside of the same directory with a randomly generated name, so you don't have to configure anything.

**8:07** · And for this branch, we're just going to use CodeX again for the sake of variety. And this is a good chance to also mention this little uh tools panel that we have at the top. If you click in here, you get this side panel that feels pretty familiar if you're coming from VS Code or something like that. So, if you missed having a file tree, for example, we have one of those. And if you also missed command shift F in order to search for things, there's one of those as well. So, in this case, I wanted to update a test file, and I'm trying to remember the name of what that was.

**8:37** · So, I could search for like skill args or something like that. And we're using Ripgrep in here, so it's very, very quick to give me results even if it's a long search. And I can also go to the file tree if I want to. We can see in here, this is the test file I'm looking for, message\_test.go.

**8:56** · We can also check in on OpenCode in a moment, but I'll just put that into the to the notification shade. And if we wanted to have the agent update this specific file, you can actually just drag it directly into the prompt box, and it'll paste the full path, which is super convenient just for like dragging in little bits of context. So, here I want to add a test to this, and I can also open up the composer or hold the function key if I want to put voice into this.

**9:23** · I want to add a test in here for handling multi-line strings when we're parsing args for skills. And that'll transcribe just as well. We can send that off.

**9:36** · And we can have the agent start working on that. And because we saw OpenCode finish, I can go check on that either from the notification shade again or from the sidebar. Wherever you want to do it, it's available. You can just see the little tasks inside of there. And we can see the changes that the agent made right inside of here. A few more lines were added. And now that CodeX is done, you can hit the code review panel and see the little changes that were made inside of here. Nice. All right, we got the basics down. What if you want to customize this setup a little bit? Maybe you want different naming for your work trees.

**10:05** · Maybe you want Claude or open code to run every time you make a new tab. Or maybe you even have preferences on how all of your panes should be divided up every time you start up Warp. All of this stuff is customizable now using this thing called tab configs. Let me show you. So, if we click on this button at the top or use this keyboard shortcut, we have a tab configs option.

**10:26** · And this will show you all of the ways that you can open a tab in Warp. Of course, you can just make a new tab and that starts terminal session. But, you also have some options to use like Warp's built-in agents or configure your own recipe. So, if I click on this right here, new tab config, this will actually pull up a file editor inside of your terminal. Warp has a file editor, by the way. I don't know if you knew that. It's kind of convenient for stuff like this where you can set up a config file that describes how your Warp window should be set up whenever you make a new tab.

**10:54** · And this is totally writable by yourself or by agents. We have a documentation reference you can point either Warp or your agent to in order to write this file for you. Or you can just kind of fill out the stubbed fields that we have right here. So, I've created a new tab config and we can already see that up here inside of this menu right here, new tab config. And I can, you know, change the name of it, for example, like new Claude session if I want to jump straight into Claude whenever I start this thing up. And you can also describe the panes that are opened up.

**11:25** · So, by default, it'll open a new terminal pane. You can describe the commands that you want to run. So, I can put Claude in here, for example. And you can also say the directory you want to jump into.

**11:35** · Like, maybe I always want to open my Warp internal directory and I change this to new Claude uh internal project or something like that. I'll go ahead and save this file with command S. And now, inside of here, I have a new tab config that I can click on. So, if I jump into this right away, you'll notice it goes into Warp internal and starts the Claude session for me. So, I don't even have to remember to do that. So, if you're constantly working on a particular coding project and you want to use your favorite agent, well, now you can just configure that as a file.

**12:06** · Now, let's say you want to go a little bit further and select which project you want to open with Claude. Well, we also have this little thing called parameters that we're experimenting with. So, you can set a directory to be a parameter instead of a hard-coded project. And this will present a little form to you every time you open a new tab to select the project to open Claude inside of.

**12:26** · And you can set the description text. You can set the type. In this case, I'm setting it to be type repo. That way, it'll pull in any of the repositories that are inside of this list right here that we were looking at earlier with work trees. This is the list of all the repositories on my computer that I registered with this button down here.

**12:43** · And let me show you what this does. So, if I wanted to start this up now with the new parameter, this will ask me before jumping in which project I want. It'll select the first repo by default, which is Warp internal, usually what I want to use. But, I now have an option to like switch over to Warp server and open a Claude session over there. Boom. Now, I'm inside of Warp server executing that Claude session. So nice. So, if you want to turn this into a Claude code workbench instead of a terminal, you can totally do that. And instead of having to like click on this button every time, you can also set defaults.

**13:13** · You may have noticed that a little bit earlier. You can remove these easily, edit the config files. Or, if I want to promote this to my default keyboard shortcut, I can say make default right there. Now, every time I do command T, it'll do the exact same menu. So, I can open the tab again. There we go. Now, I'm inside of Claude.

**13:31** · So, however you want to customize this thing, totally works. And just to show you how capable this is, you can configure just about anything you want in that window. For example, if you have split panes that you often use, you can describe all the panes that you want to open. So, here I've set something up that will spin up a Claude session on the left to work on my client application and a server on the right that's going to start up our server connected to that client build. So, when I'm ready to jump in and test something, I already have the server spun up and ready to go.

**14:02** · And you can set that up with split panels so that it's on the right and on the left. You can set it with children right here, split horizontal. It's all configurable. So, if I wanted to add a internal plus local server, I can click on this and it'll start that up for me. So, now we have Claude on the left and the server running on the right ready for me to work on. You can also use this to customize the work tree naming convention. So, earlier we showed the built-in work tree setup which creates a randomized name inside of the outer directory.

**14:30** · You might want to customize that to be a different directory, different naming convention, whatever. Well, you can just set up the commands you want to run to use get work trees.

**14:40** · So, for example, I modified that Claude code picker to also spin up a work tree for me at the same time. So, I added a command ahead of starting Claude to also add in a work tree. We have a special character in here to generate the branch name for you. And I specified that I want my work trees to go in this directory instead. So, now everything will go inside of work trees. Have a few more commands actually grab the project name so it's very smart about that. And everything else remains the same. So, let me show you how this works.

**15:06** · If I click on this or just use command T since it's now my default, I can click on Claude work tree, select Warp internal. That'll generate the work tree and start up Claude code inside of there instead.

**15:20** · And just a little bonus tip, if you want to set the name of the tab so it's not just generated name or the generated conversation, you can click on this and change it. So, you can just double-click and edit to be like work tree for \[snorts\] new feature. So, now you can easily hover around and find that. You can also go further in customizing this tab bar.

**15:41** · Right now, I'm using uh the tab setting, but if you want to view the individual panes inside of a tab, you can also expand it by clicking on panes. And this will show you not only the specific terminal tabs, but also multiple split panes that you have open. So, here it shows me I have a file on the right and terminal on the left. And all that's expanded for me to quickly view it. You can also switch to tabs if you prefer just seeing the currently focused tab.

**16:06** · You can also change the density. This will just add some more metadata on there. So, if you want to see both the branch name as well as the directory name, that'll expand it out nicely. If you just want it to be compact, you can do that. And of course, you can tweak it to your heart's content. Like, if you always want to show the working directory instead of a generated conversation name, you have that right there. You also have choosing branch or working directory in this little compact mode. And you can show and hide those details on hover. I personally find this very useful so I can get context on what an agent's doing.

**16:36** · But, if you find hover hints annoying, you can turn them off as well. And if you have ideas on how you want to tweak this that we haven't thought of yet, definitely let us know. All right, we've covered the full gamut.

**16:46** · Running any agent inside of Warp, playing around with the input, voice input mode, the code review panel, and also managing all of those agents with the vertical tab bar and work trees and custom tab configs to describe exactly what you want to happen every time you spin up a new agent. If that sounds useful, just download the app. It's free to download. You can use it without an account, warp.dev, and you can start running whatever agents you want.