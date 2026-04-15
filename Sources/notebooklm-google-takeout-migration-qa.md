# Source: NotebookLM Google Takeout Migration Q&A

**Ingested**: 2026-04-15
**Type**: Q&A / Community Knowledge
**Status**: immutable

---

**Question:** I used Google Takeout to download all my NotebookLM data from one Google account. How can I import it into another Google account?

**Answer:** The short answer is: You cannot directly import a Google Takeout file into a new NotebookLM account. NotebookLM does not currently have a native "import" or "restore" feature for automatically migrating entire notebooks from one account to another.
However, you can still move your data over manually using the files you downloaded. Here is the most efficient way to get your information into your new account:
1. Extract Your Takeout Data
First, unzip the file you downloaded from Google Takeout. Inside, you will typically find your data organized into folders containing:
Your uploaded source content (PDFs, text files, etc.)
Generated notes
Chat history (often in JSON format)
Generated Audio Overviews


2. Manually Recreate Your Notebooks
Since there isn't an automated migration tool, you will need to rebuild the notebooks in your new account.
Log into NotebookLM with your new Google account.
Create a new notebook.
Re-upload your sources: Manually drag and drop the original source files (PDFs, text files, etc.) from your unzipped Takeout folder into the new notebook. Note: If your original sources were Google Docs or Google Drive files, you will need to share those files with your new Google account and import them directly from Drive.
3. Preserving Notes and Chat History
Because chat histories and notes export as raw data, they will not automatically populate back into the NotebookLM chat interface or note board.
The Workaround: If you have important chat logs, summaries, or generated notes you want the AI to remember, combine that text into a single Google Doc or Markdown (.md) file.
Upload that newly created document as a source in your new notebook. This ensures the AI in your new account has all the historical context, insights, and notes from your previous sessions.
Pro Tip: If your chat history exported as a dense JSON file, there are community scripts available on platforms like GitHub (search for "NotebookLM JSON to Markdown") that can automatically convert your Takeout JSON data into clean Markdown files, making them much easier to read and upload as new sources.
