In summary, the most interesting aspect is the automation of knowledge base maintenance through AI, enabling self-improvement and continuous updates without manual intervention.

## Headlines

- **AI-powered wiki automation:** Scheduled context farmers autonomously scrape sources like YouTube and Slack, ensuring the knowledge base remains updated without manual intervention.
- **Integrated MCP connectors:** These connectors facilitate the autonomous scraping of data from various applications, feeding the AI wiki.
- **Cloud deployment:** Farmers can be deployed in the cloud using GitHub, allowing for continuous operation and updates even when the user is offline.

## Things

- People:
  - Brad (presenter)
  - Andrej Karpathy (concept inspiration)
- Places:
  - Cloud (for deployment)
- Things:
  - AI Wiki
  - MCP connectors
  - Context farmers
  - YouTube
  - Slack
  - GitHub
- Concepts:
  - Self-improving knowledge base
  - Automated content updates
  - Scheduled scraping
  - AI-powered automation

---

![](https://www.youtube.com/watch?v=nilNHl4uZcU)

## Transcript

### Intro

**0:00** · Andre Karpathy's LLM Wiki is a great idea with one problem. You have to remember to update it. The moment you stop manually feeding it new context, it stops knowing anything and your new Wiki becomes basically useless. So, I gave it the ability to grow new context automatically. Now, it watches every app that I care about, pulls in new context on its own, and grows the Wiki without me ever touching it. And it's saving me more time than ever because it's always up to date.

**0:25** · Right now, I'm going to show you exactly how I built this, how to set it up for yourself, and how to deploy 24/7 context farmers that are constantly mining your apps for data, all within Claude Code. Plus, I'm giving you a Wiki Builder skill that does the entire setup for you. I've set this demo up with a Karpathy Wiki to keep track of all of my favorite AI content creators, what they're posting, and what's getting results. Every creator I track has their own page with what they cover. There's a summary for all their reoccurring ideas and what they like to cover.

### Demo: the self-updating wiki

**0:53** · I'm even getting all of their generated thumbnails and transcripts automatically in the raw folder. I haven't made a single one of these. Each creator page updates itself when they drop a new video. And at a drop of a dime, I can go to the graph page and search for anything, whether that's N8N, Claude Code, or absolutely anything. Each creator page updates itself whenever a new video drops. The context farmer goes out and grabs the transcript and the thumbnail, brings it in, and ingests it into the knowledge lab.

**1:23** · Over time, the Wiki gets richer and richer, and the interconnected layers get stronger and stronger. And because it's all markdown in Obsidian, I can drop this into any Claude Code session and have full context whenever I'm doing my content planning. This Wiki grows totally automatically. Every day, context farming sub agents are adding in more and more videos, more relationships, and more knowledge. And all of this feeds into the content decisions I make. This is the type of leverage you can get when you remove human ingestion as the bottleneck to your context layer. This Wiki grows totally automatically.

### How a Karpathy wiki is structured

**1:53** · So, a quick recap if you haven't seen one of these Karpathy Wiki set up. It's just two folders, a raw folder and a Wiki folder. You drop sources into the raw folder, and the LLM ingests those and builds out Wiki pages inside of the Wiki folder. Inside of the Wiki folder, you also have an index and a log. The index keeps track of all of the relationships between all of the files, and the log keeps track of the updates that the LLM makes. So, I've got a totally fresh Wiki here. It's completely empty.

**2:21** · And instead of manually dropping in files into raw, I'm going to set up what I'm calling a context farmer, an AI agent that connects to source through MCP, in this case Appify, and does the fetching for me. And we're going to start with YouTube. So, I've already got my context farmer inside of Claude Code Cloud. And every day at 6:00 a.m., it goes out and scrapes all of the channels that I'm interested in, finds what videos they've posted, pulls their transcripts, gets their thumbnails and their stats, and adds it into my raw folder, all without me having to do anything.

### Building a YouTube context farmer

**2:52** · So, let's run it now. It's going out and using a YouTube scraper to find all of the recent videos since it last ran and pulling them into my Karpathy Wiki. From there, it's adding it into the raw folder, and then it will ingest them into each of the interlinked context documents. And there we go. It looks like there's been two new videos posted today, and it's pulling those into the raw folder now. Now, watch what happens.

**3:16** · The context farmer is about to go in and create the interlinked pages, assigning each of the new videos to the creator that posted them, updating the index file and the log file, and automatically growing the Wiki so I know more and more about what content is being posted about AI on YouTube. So, now the LLM is reading through all of the transcripts and the thumbnails and building out pages inside of my Obsidian Wiki. It's pushing the updates to GitHub because this is a cloud context scraper, and my Obsidian will automatically pull those updates to my local machine so I can use them with Claude Code.

**3:45** · So, Claude has created two new video pages, one for a video by Nate Herck and another one from Nate B. Jones. And now that the context farmers have made the changes inside of GitHub, the Obsidian Git plugin is automatically pulling those changes down to my local machine. I can go to the Nate Herck page inside of Obsidian, go scroll down, that his most recent video has been automatically linked. I can even click through to that and see all of the details about his plugin video that he just posted. I can even go to my graph page, and now these nodes are automatically connected. And here's the really important part.

**4:16** · Tomorrow, when the farmer runs again and pulls new videos, the Wiki doesn't start over. It updates. If someone drops a follow-up video on that topic, that page gets richer. New connections form and the whole thing compounds over time. I'll even show you how powerful this is when you pair the Wiki with Claude Code. I have the Wiki open up in my Claude Code, and I'm going to ask it, "What was the most recent videos that were posted by Nate Herck, and what topics did it cover? Has this topic been covered by anyone else inside of your Wiki?" I can ask ad hoc queries of this context layer at any time.

### Querying your wiki inside Claude Code

**4:47** · This is so important for me when I'm doing my content research because that way I can see what's already being covered, how people are talking about certain features, and all of this feeds into my content. And I can see that Nate Herck posted a video about a new Claude plugin called Superpowers.

**5:03** · I can see all of the other videos from the creators that I'm tracking that reference similar types of content, and I can get that all at the touch of a button inside of Claude Code. I can even ask it about new topics like Claude managed agents, which was just recently released. What are people saying about Claude managed agents? And just like that, I can get the two perspectives of videos that have been posted about managed agents, one by Nate Herck and another one by Nick. And Claude's already analyzing how each creator is covering the topic and where the gaps might be. So, that's what I'm calling context farming. And here's the key insights that makes this work.

### Taste vs fetching: why this works

**5:35** · Karpathy's whole thing is that LLMs have bad taste. They can't tell you what's worth reading. And he's right. You don't want an AI randomly scraping the internet and dumping garbage into your knowledge base. That's how you end up with a Wiki full of noise. But there's a difference between selecting sources and fetching them. Selecting is the taste part, the human job. You decide, "I trust this YouTube channel or this Slack workspace matters." That's the judgment and curation, and you only do that once.

**5:59** · But once you've made that call, everything after is just fetching. It's pulling the latest video, grabbing the transcript, checking new messages, and that's not taste. That's a cron job. And that's what context farmers handle. So, you keep the human creation that Karpathy's right about, but you stop doing the manual grunt work that kills every Wiki. Anything with an MCP connector can become a source, whether that's Slack, Fireflies, YouTube, Notion, or whatever. You pick the sources, set up a farmer for each one, and schedule it, and the Wiki just stays fed. So, that's AI YouTube, but here's where it's actually going to get interesting.

### Farmers for Slack, research, and competitors

**6:29** · This pattern works for literally anything that has an MCP connector. For instance, business context. I set up a farmer on my Slack channels and my Fireflies meeting transcripts, and now the Wiki just briefs me. Customer renewals, project status, decisions that got made in meetings that I wasn't even on. I walked into a customer call the other day fully prepared, and I hadn't read a single Slack message. If you want to see how that whole thing works step by step, I actually did a full video on it, and I'll link it here. Or even research. You could set up a farmer that scrapes for new papers in whatever field you're in.

**7:00** · Claude reads them, builds concept pages, and tracks who's publishing what. And it'll even flag when new findings contradict stuff that's already in the Wiki. Or how about competitive analysis?

**7:09** · Farmers on your competitors' blogs, their social accounts, and their job posting. You end up with a Wiki that's just tracking their moves for you. The pattern is always the same though. Okay.

### Running farmers in the cloud with GitHub

**7:19** · So, one thing you're probably thinking is that if your farmer is running on your laptop, then your laptop has to be open, right? And yeah, that does work.

**7:26** · But if you want to get this thing running while you sleep, you need somewhere for your context layer to live. And that's where GitHub comes in.

**7:32** · The Wiki lives in a private GitHub repo.

**7:35** · Claude hooks auto commit and auto push every time a farmer drops new files into raw. So, the Wiki is always synced to the cloud, and anyone you give access to can pull from it. So, it's not just your Wiki anymore, it's everyone in your organization's Wiki. And then for scheduling, Claude Code has built-in scheduled agents. You can set a time, give it the farm prompt, and it runs on Anthropic's infrastructure. It clones your repo, runs the farmer using an MCP connection, and commits the new sources and pushes, all in the cloud. So, here's my setup. I have my YouTube farmer running at 6:00 a.m. every day.

**8:05** · I have my Slack farmer running at 6:30 and the Fireflies farmer running at 7:00. That's why every morning when I log in, I have new context sitting in raw ready to digest. And it doesn't matter if my laptop was overnight. My context layer just keeps getting smarter and smarter every time it runs. Now, if you've got farmers that use local tools like any type of CLI or custom pet scripts, you can schedule them from Claude Code desktop as well. You just need to go to the new local task button, and that task will now run on your machine. The only caveat is that your laptop needs to be on for them to run.

**8:36** · Just think about this for a second. If you have a Wiki that tracks everything happening in your industry, and another one tracking your competitors, you might even have one tracking your customers. You begin to have a fully enriched context layer across everything that you're interested in. And all of them are running without you touching everything. Every MCP connector and every app becomes a potential source for context, and there are hundreds of them in the connectors tab inside of Claude. Okay. So, if you want to set this up for yourself, I actually built a Claude Code skill that does the whole thing for you, and the link's in the description. It's totally free.

### What a fully farmed context layer unlocks

### The free Wiki Builder skill

**9:07** · All you have to do is just install the skill into your dot Claude folder inside of your repo. You tell it what you want, and Claude will actually build out the Wiki custom for your requirements, whatever you need. It'll ask a few questions, figure out the right sources, and all of that goes into your Karpathy Wiki. It even builds the context farmers for each source and wires them up for scheduling. You don't have to do any of it yourself. I'd also recommend opening up the Wiki inside of Obsidian. It's optional, but honestly, the graph view and the backlinks are totally worth it. And then, you've got a choice.

**9:37** · You can run your farmers locally, which is fine for getting started, or you can schedule them to run as always-on in the cloud. The skill walks you through either path. I want to build a Wiki for keeping track of all of my favorite creators on YouTube. I want to provide you a few channels, and then from there, you'll set up a context farmer, which will go and find those YouTube channels new videos every single day and then fold them into the wiki as well.

**10:03** · I want to use Appify for the context farmer. The skill is trained on Kapathy's LLM wiki framework and it talks you through everything that you need to get started. You can select the full build, the wiki and farmers, or just the wiki. I always go for the full build because that way I can set up my context farmers to run in the cloud. And then you've got a choice. You can run the farmers locally, which is fine for getting started, or you can schedule them to run always on in the cloud. The skill walks you through either path. And then just let it run. Every day your farmer pulls new context, the wiki ingest it, and pages compound. You literally wake up smarter.

**10:32** · Pick a topic, connect a source of truth with an MCP, and schedule a farmer and the wiki handles the rest. This was a super quick setup guide, but if you want a full breakdown, there's a setup guide linked at the description below, as well as a video linked here that walks through it in a little bit more detail. If you want help deploying this for your business, I do AI strategy sessions where I map the whole thing to your stack. Links in the description below. I'm also building a marketplace for verified Claude code skills. Production-ready, vetted by real domain experts.

### Outro

**11:01** · And if you want early access, the waitlist link is in the description below. Again, thanks for watching.