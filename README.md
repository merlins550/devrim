# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

## Copilot Chat

A simple desktop chat interface is provided in `copilot_chat_ui.py` for interacting with GitHub Copilot.

1. Install Python dependencies: `pip install -r requirements.txt`
2. Export your Copilot token: `export COPILOT_TOKEN=your_token_here`
3. Run the chat UI: `python copilot_chat_ui.py`

The UI automatically loads project metadata and TODO notes as context for Copilot.
