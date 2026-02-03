# ai-agent-app2

A small AI agent demo project with a Vite + React frontend.

## Overview

This repository contains a frontend built with Vite and React. It includes a simple chat UI and pages for different agent types.

## Quick start (frontend)

From the project root run:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## Project structure

- `frontend/` — Vite + React frontend source
  - `src/` — React source files
  - `public/` — static assets

## Contributing

Feel free to open issues or pull requests.

## License

This project has no license specified. Add one if you plan to share the code publicly.

## Deployment to Heroku

Two common ways to deploy this Vite + React frontend to Heroku are shown below. Choose the one that fits your workflow.

Option A — Use the Heroku static buildpack (quick, no server code)

- Install the Heroku CLI and log in:

```bash
# macOS (Homebrew)
brew tap heroku/brew && brew install heroku
heroku login
```

- From the project root, create the app (replace `your-app-name` if desired), set the static buildpack, and push:

```bash
cd /path/to/ai-agent-app2
heroku create your-app-name
heroku buildpacks:set https://github.com/heroku/heroku-buildpack-static.git
git push heroku main
```

Notes:
- If your production build is in `frontend/dist`, the static buildpack will serve files from the repository root. You may need to add a `static.json` to configure the buildpack or move the `dist` output to the repository root before pushing.

Option B — Serve the built site with a small Node server (recommended when you want a simple Node process)

1. Add a small server (example `server.js`) at the repository root that serves the `frontend/dist` folder:

```js
// server.js
const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, 'frontend', 'dist')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'dist', 'index.html'));
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server listening on ${PORT}`));
```

2. Add a root `package.json` (if you don't already have one) with a `start` script that runs the server. Example minimal `package.json`:

```json
{
  "name": "ai-agent-app2-root",
  "version": "1.0.0",
  "main": "server.js",
  "engines": {
    "node": "16.x"
  },
  "scripts": {
    "start": "node server.js",
    "heroku-postbuild": "cd frontend && npm install && npm run build"
  }
}
```

The `heroku-postbuild` script builds the frontend after Heroku installs dependencies.

3. Commit `server.js` and the root `package.json`, then create the Heroku app and push:

```bash
git add server.js package.json
git commit -m "Add Heroku server + build script"
heroku create your-app-name
git push heroku main
```

Heroku will run `heroku-postbuild`, which builds the frontend into `frontend/dist`, and then the `start` script will run the Node server to serve the static files.

Troubleshooting and tips
- If you see routing problems on refresh, ensure your server returns `index.html` for unknown routes (see the `app.get('*', ...)` example).
- Use the Heroku dashboard or `heroku logs --tail` to inspect runtime logs.
- For a production static site without a server consider using Netlify, Vercel, or GitHub Pages which are simpler for static frontends.

If you want, I can add the `server.js` and root `package.json` for Option B and commit them to the repository — tell me if you want that and what `node` version you prefer.
