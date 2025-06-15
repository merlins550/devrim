# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

## Repository Layout

- `matrix_ai/` contains the Python modules
- `web/` contains the web front‑end
- `docs/` holds documentation and misc files
- `scripts/` includes helper scripts
- `tests/` has the unit tests

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. (Optional) Set a `GITHUB_TOKEN` in `.env.local` if you want to enable the
   GitHub API features used by some scripts.
4. Run the app:
   `npm run dev`

## Automation

Pull requests labeled `codex` are automatically approved and merged by a GitHub Actions workflow.
The workflow installs dependencies, runs `scripts/auto_fix_python.py` for formatting, executes the
unit tests, and merges the change if everything passes. A `GITHUB_TOKEN` secret is required for the
automation.
