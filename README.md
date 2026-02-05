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

## Quick start (backend - Flask API)

The backend is a Flask server that serves the React frontend and provides AI agent endpoints.

### Local development

From the project root:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set your Groq API key
export GROQ_API_KEY="your-groq-api-key-here"

# Run the Flask server
python3 main.py
```

The server will start on `http://localhost:5001` (or the PORT environment variable).

### API Endpoints

- **`GET /`** — Serves the React frontend (index.html)
- **`GET /<path>`** — Serves static assets and SPA routing
- **`POST /api/research`** — Research agent endpoint
  - Request body: `{ "message": "your query" }`
  - Response: `{ "response": "agent response" }`

### Backend Architecture

#### Main Files

- **`main.py`** — Flask application server that:
  - Serves the built React frontend from `frontend/dist/`
  - Provides API endpoints for AI agents
  - Handles CORS for frontend communication
  - Configures caching headers for production

- **`agents/`** — AI agent implementations:
  - **`base_agent.py`** — Base class for all agents using Agno framework and Groq models
  - **`research_agent.py`** — Specialized agent for research queries, technology comparisons, and industry trends

#### How It Works

1. The Flask app initializes with CORS enabled for cross-origin requests
2. User sends a message via the React frontend
3. Frontend calls the appropriate API endpoint (e.g., `/api/research`)
4. Flask receives the request and instantiates the corresponding agent
5. Agent processes the query using Groq's LLM (llama-3.3-70b-versatile)
6. Response is returned to frontend and displayed in the chat UI

#### Agent Classes

**BaseAgent** — Foundation for all agents:
- Initializes a Groq language model
- Provides `get_response()` and `print_response()` methods
- Supports streaming and non-streaming responses
- Stores agent name, description, and avatar

**ResearchAgent** (extends BaseAgent):
- Implements research-specific methods
- Supports web search queries
- Provides technology research and comparison
- Analyzes industry trends

#### Environment Variables

The backend requires:

```
GROQ_API_KEY="your-groq-api-key-here"
```

Add this to a `.env` file in the project root (not committed to git for security).

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
