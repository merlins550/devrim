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
- Commit message generation with HuggingFace `smolagents` when `USE_SMOLAGENTS` is enabled
- GitHub API operations rely on the `requests` library

Refer to `TODO.md` for remaining tasks.

## VS Code Setup

The assistant relies on the VS Code `code` command for Copilot integration.
If VS Code is installed in a non‑standard location, you can override the
executable path with the `VSCODE_PATH` environment variable.

### Default locations

| Platform | Path |
| --- | --- |
| **Windows** | `C:\Program Files\Microsoft VS Code\Code.exe` |
| **macOS** | `/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code` |
| **Linux** | `/usr/share/code/bin/code` or simply `code` in your shell |

### Copilot requirements

Install the GitHub Copilot extension in VS Code and ensure the `code` command
is available in your `PATH`. On Windows you can enable this via the
`Shell Command: Install 'code' command in PATH` command from the Command
Palette.
