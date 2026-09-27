# BrandForge AI v3

Strategy-first personal brand architect for the Inkloom challenge.

## What this build contains

- staged Discover → Research → Position → Shape → Visualize → Content → Challenge → Deliver workflow
- optional OpenAI Responses API integration
- optional live web research via Tavily
- clear fallback mode when API keys are missing
- SQLite persistence
- PDF export
- AI critic + revision loop
- source cards for live research
- polished React/Vite interface

## Run backend

```bash
cd backend
python -m venv venv
# Windows
venv\\Scripts\\activate
# macOS/Linux
# source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
# macOS/Linux: cp .env.example .env
uvicorn main:app --reload
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL, normally http://localhost:5173.

## API keys

The app runs without API keys using clearly labelled fallback logic.

For live AI, configure `OPENAI_API_KEY` in `backend/.env`.

For live web research, configure `TAVILY_API_KEY` in `backend/.env`.

Never commit `.env` or API keys to GitHub.
