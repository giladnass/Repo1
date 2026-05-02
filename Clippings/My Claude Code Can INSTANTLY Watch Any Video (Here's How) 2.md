In summary, the most interesting aspect is the ability to process video frames and audio transcripts locally, enabling AI models like Claude to 'watch' any video without relying on external APIs or incurring high costs.

## Headlines

- **Local Video Processing:** Enables 'watching' any video by processing frames and transcripts locally, bypassing external API limitations.
- **Cost-Effective Analysis:** Achieves significant cost savings compared to API-based transcription services, with an estimated cost of about a dollar per run.
- **Comprehensive Context Extraction:** Captures visual information from video frames in addition to audio transcripts, providing a richer understanding than text-only analysis.
- **Efficient Workflow Integration:** Streamlines content consumption by automating the process of extracting information from videos, saving time on manual scrubbing and re-watching.

## Things

- People:
  - Brad (creator)
- Places:
- Numbers:
  - 1000+ (sites supported by yt-dlp)
  - $1 (estimated cost per run)
  - 2 minutes (processing time for a 45-minute lecture)
  - 5 minutes (installation time)
- Things:
  - Claude Code
  - YouTube-DL
  - FFmpeg
  - MP4
  - YouTube link
  - Instagram reel
  - Loom
  - Frames
  - Audio transcript
  - Groq Whisper
  - Obsidian
  - GitHub
  - AI agent skill
- Concepts:
  - AI automation
  - Local video processing
  - Content intelligence
  - Context engineering
  - Workflow integration

---

![](https://www.youtube.com/watch?v=QZMljuD10sU)

## Transcript

### Intro

**0:00** · When you give Claude code the ability to instantly watch any video on the internet for free, it becomes genuinely unstoppable. With this Claude skill, Claude can understand video as well as it reads PDFs. Hours long YouTube videos, Instagram reels, Looms, local files, anything. Before Claude was just guessing, now it can watch the whole thing frame by frame instantly. It's like Neo plugging into the Matrix. By the time you've hit play, Claude's already watched the whole thing and become an expert. a bunch of transcript tools before developing this one and they all let me down.

**0:30** · They either cost way too much or they only ever read the transcript and missed half the video.

**0:36** · This skill gives Claude the frames and the audio together, so it actually sees what's happening on screen. Right now, I'll walk you through exactly how it all works. The use case that completely changed how I consume content and how to set this up in your own Claude code in under 5 minutes. Here's what it actually looks like on a 45-minute video done in less than a few minutes. On the left, I have a YC lecture from Sam Altman about how to start a startup. I'm going to press play on that now and then grab the URL. All I have to do is go over to Claude and type {slash} watch and then paste the URL here.

### Watch Videos in Minutes

**1:07** · Then Claude gets to work grabbing the subtitles from YouTube for free, extracting the frames and analyzing them all together. So, the reason this is better than just pulling the transcript is because Claude can actually grab the frames from this video. In this lecture, Sam goes through and shows a bunch of really great graphs. And this is important context for Claude because if you're only getting the transcript, you're only getting half of the information. Now, here's where most of the existing video tools fall short because they base everything around the transcript.

**1:33** · When something happens on screen and it's not explicitly referenced in the transcript, Claude doesn't know about it and you miss out on key context, which matters because half of the interesting stuff in video isn't said out loud. It happens on screen. So, this skill actually watches.

**1:48** · It pulls frame by frame screenshots and puts it together with a per second timestamped transcript to get Claude the full picture and full context. And just like that, we're only 2 minutes into the lecture. Sam is still introducing what he's going to talk about today and Claude has already ingested the entire thing. I have a structured summary of all of the speakers. I can see exactly what they talk about and now I can actually query Claude on anything about this context and then start to put it to work instantly right here in the terminal. That's a 45-minute video done in less than 2 minutes.

**2:20** · Watched, analyzed, and applied. That's the Matrix moment. You're not watching content anymore. downloading context automatically and putting it to work straight away. And you're probably thinking at the moment there's some expensive API doing the heavy lifting here, but there isn't. But before we get into that, let's get into the setup. By the way, I'm giving this whole skill away for free on GitHub. The link is in the description below. Just run these install commands and the setup takes care of the rest. Once the skill is installed, Claude runs the setup script and installs any dependencies that you don't have already.

### Setup

**2:52** · It authenticates with the transcription API. Don't worry, this one is pretty much free and we'll get to it in a second. But under the hood, the pipeline is actually surprisingly simple. Now, here's the part that nobody really talks about.

**3:04** · Claude can't actually watch video because Anthropic doesn't have a video model yet. There are some other providers that can, like Google's Gemini model, but they're pretty expensive and they don't integrate nicely with Claude.

**3:15** · So, if you're watching a lot of content, that bill stacks up pretty fast.

**3:18** · Luckily, there's a smarter way to do this because if you really break it down, a video is just two things. It's a bunch of frames and the transcript.

**3:24** · That's it. So, instead of paying for another expensive model, I can just split the video into those two pieces and hand it to Claude in a format that it already knows how to read, pictures and text. Now, this is the part I love because the skill is doing this with two of the oldest, most battle-tested command-line tools on the internet, YouTube-DL and FFmpeg. These aren't MCPs. They're not some new wrapper.

### Under the Hood

**3:44** · There's no third-party service involved in the middle here. They install once, right on your machine. Millions of developers have used them for over a decade now. They're rock solid and completely free. And they're what every video tool you've ever touched is probably using under the hood. YTDL is the download. You can think of it as a right-click save video, but it works on basically the whole internet. FFmpeg is the video engine. It takes the video and turns it into two things that Claude actually wants. First, screenshots, which are taken every few seconds all the way through the video.

**4:11** · And then second, the audio file, which is pulled out as a clean little file ready to be transcribed into text using Whisper.

**4:17** · Now, Claude has the full picture when we put these two together. It's flipping through the screenshots like a flipbook, reading the transcript like a script, and the timestamps line up exactly, so it knows on screen when something is being said. So, that's the whole pipeline. YouTube-DL and FFmpeg doing all the heavy lifting locally on your laptop for free. The only thing we actually have to pay for here is the transcription and Claude usage. Captions transcription is pretty much free. The skill just pulls them. And if it doesn't, it transcribes the audio using Whisper hosted on Grok or OpenAI.

**4:44** · I prefer Grok because it's extremely fast and their free tier covers basically anything you throw at it. So, most videos cost you literally nothing to transcribe. I even used this exact skill to grow Universal Context Layer for content research and I'll show you exactly how it works in a minute. And I can literally hear the keyboards clattering right now, Brad, this is going to torture your token budget. This actually surprised me, so let's do the math. The skill scales frame count to video length and it actually caps anything over 30 minutes to 100 frames.

**5:13** · So, a 30-minute video and a 1-hour video pretty much cost the same amount in dollar terms. And that's about $1 per run. I ran every test in this video three times in parallel and burned less than 10% of my session. And that's over 5 hours of video watched live by Claude with transcription. And the transcription part's where it gets ridiculous. Every YouTube video comes with a free transcript. The skill just pulls them. There's no Whisper, no API call. It's totally free. And that goes for a bunch of other sites, too. Whisper only kicks in for the stuff without captions, like a raw MP4, a Loom, or Instagram reel.

### The Cost Math

**5:44** · Grok's free tier actually gives you 2 hours of transcriptions per hour, which covers more than you'll realistically throw at it. I've used this skill every day for 2 weeks and I'm still on the free tier.

**5:55** · It's crazy. Look, I'm not saying this is perfect and there's probably optimizations I haven't thought of, but for most people watching, this is essentially free. If you got ideas to make it cheaper or quicker, drop them in the comments below. Once I realized this was basically free, I started running it on everything, which is how I ended up building the system I'll show you at the end. And it's one that's genuinely changed how I consume content. Here's the part that actually makes this skill a must-have. It works on any URL YTDL supports, which is over 1,000 sites.

**6:24** · This isn't just limited to the big social media companies or YouTube. And it even works if you have the files locally downloaded. So, that opens up a bunch of use cases that you probably wouldn't expect. So, this is what I'm doing for content research now. I take a a winning video from the internet and I ask Claude to break down the hook.

### Analyze Video Hooks

**6:40** · Claude tells me the visual setup, the exact words, where the pattern interrupt lands, and what's on screen at the moment of the hook. Stuff that used to take me 10 minutes per video, pausing and scrubbing, now it's just a paste.

**6:50** · And for developers, there's another use case, debugging screen recordings. If you're a developer and a UI bug shows up, you record a 30-second screen recording, drop it into Claude, and ask what happens right before the crash.

**7:02** · Claude reads the frames around that moment, finds a state change, and tells you the exact frame the issue starts with. That alone has saved me hours. The skill also has a zoom flag, start time, and end time, so you can drop those in and Claude can focus frame-by-frame extraction on a specific window of a video. So, you can ask about a 10-second segment of a 2-hour video without burning your entire context window.

### Review QA Videos

**7:22** · Whatever you're using video for, you can probably stop watching it manually because of this skill. So, earlier I told you that once you start using this thing, it seriously starts to change how you consume content. Now, I want to show you my personal favorite use case for it, which is feeding my second brain. I keep a knowledge base in Obsidian with notes, snippets, and ideas for content.

**7:40** · And the bottleneck for me has always been throughput because there's just so much good content out there by creators at the moment, there's not enough time to watch it all and write it all down.

### Content Intelligence

**7:47** · So, I let Claude do both. I give it every single competitor that I think makes great content and then from there, Claude uses the watch skill to automatically watch it and feed it straight into my second brain. So, Claude watches each of these videos, frames, audio, everything, and then comes back with a clean structure and notes about what made the video work. It fills that straight into the second brain. And this is where things start to compound because the skill and your second brain are watching more and more videos, getting more and more context, and it's getting better and better over time, getting smarter automatically. The second brain side of this whole thing is a video on its own.

**8:19** · And I walk through exactly how I run mine, content research, competitor intel, every podcast video I've ever listened to, all in one searchable layer in Obsidian. If that's where you want to take this, that's the next video to watch. It's linked up here. If this was useful, hit subscribe. Thanks for watching and I'll see you in the next one.