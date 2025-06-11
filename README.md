# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

## Copilot Lite Chat

This repository includes a small desktop UI for interacting with your GitHub Copilot subscription. Ensure that Visual Studio Code and the Copilot extension are installed and that the `code` command is available in your system PATH.

Start the chat interface with:

```bash
python copilot_chat_lite.py
```
