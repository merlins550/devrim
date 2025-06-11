# Devrim

Matrix AI Desktop Assistant project.

This assistant launches a Selenium-based stealth browser with cookie
persistence and integrates with ChatGPT, VS Code, and GitHub.

## Configuration
VS Code integration uses the `find_vscode_path` helper which currently
searches only common Windows installation locations. If you are on a
different platform:

1. Open `matrix_ai_desktop_assistant.py` and locate the `default_config`
   dictionary.
2. Under the `vscode` key set `workspace_path` to your project folder
   and add a `path` entry pointing to the `code` executable on your
   system.
3. Alternatively modify `find_vscode_path` to return the correct path
   for your OS.

Without a valid path the VS Code Lite feature will not start.

You can optionally enable GitHub Copilot by keeping the
`github.copilot` extension in the `extensions` list. Removing this entry
will start VS Code without Copilot.

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

Refer to `TODO.md` for remaining tasks.
