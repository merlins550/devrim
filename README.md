# Devrim

Matrix AI Desktop Assistant project.

This assistant launches a Selenium-based stealth browser with cookie
persistence and integrates with ChatGPT, VS Code, and GitHub.

## Features
- Stealth browser agent with cookie management
- Optional encrypted cookie storage via `COOKIE_ENCRYPTION_KEY`
- Cookie rotation via `COOKIE_DIR`
- Customize cookie file paths with `COOKIE_FILE_PATH` and `COOKIE_JSON_PATH`
- Random user-agent selection for each session
- Optional Chrome extension loading via `CHROME_EXTENSION_PATH`
- GUI fallback between PySide6, CustomTkinter, or terminal
- VS Code Copilot integration via `CopilotBridge` without direct API usage
- Auto-detects VS Code binary on Windows, Linux (`/usr/bin/code`, `/snap/bin/code`) and macOS (`/Applications/Visual Studio Code.app/...`)
- Override detection with the `VSCODE_PATH` environment variable for custom installations
- Commit message generation with HuggingFace `smolagents` when `USE_SMOLAGENTS` is enabled
- GitHub API operations rely on the `requests` library

Refer to `TODO.md` for remaining tasks.
