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
- Commit message generation with HuggingFace `smolagents` when `USE_SMOLAGENTS` is enabled
- GitHub API operations rely on the `requests` library
- Set `VSCODE_PATH` if VS Code is installed in a custom location

Refer to `TODO.md` for remaining tasks.
