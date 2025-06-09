# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

This project also integrates a lightweight Windows 95 UI layer via
`gemini95Framework.ts`. The module exposes helpers like
`createOpenAppsMap()` and `createDosInstances()` for managing open
windows and DOS emulator instances in a type-safe way.

Additional utilities:
- `ip_rotator.py` for rotating proxy addresses
- `captcha_solver.py` placeholder for solving captchas
- `rate_limiter.py` to throttle automated actions
- `dom_interaction.py` convenience wrappers for Selenium
