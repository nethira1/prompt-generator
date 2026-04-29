# Prompt Generator - Project Architecture

## Overview
A web application that generates optimized AI prompts using the Gemini API.

## Components

### 1. Backend API (`app.py`)
- **Port:** 5000
- **Framework:** Flask + Google Gemini API
- **Endpoint:** `POST /v1/chat/completions`
- **Input:** `{"prompt": "...", "variations": 5}`
- **Output:** `{"variations": ["...", "...", ...]}`
- **Model:** `gemini-2.0-flash`

**Start:**
```bash
python app.py
```

### 2. Frontend UI (`prompt_generator.py`)
- **Port:** 3001
- **Framework:** Flask + HTML/CSS/JS
- **Calls:** Backend API at `http://127.0.0.1:5000/v1/chat/completions`
- **Routes:**
  - `GET /` → Serves HTML UI
  - `POST /api/generate-variations` → Calls backend to generate prompt variations
  - `POST /api/test-prompt` → Tests a prompt via Gemini

**Start:**
```bash
python prompt_generator.py
```

### 3. UI Frontend (`prompt_generator.html`)
- Responsive web interface with gradient design
- Two-column layout:
  - Left: Original prompt input + generate variations
  - Right: Test prompt variations
- Copy and test buttons for each variation
- Real-time response display

## How It Works

1. User enters a prompt in the UI
2. Frontend sends to `prompt_generator.py` → `/api/generate-variations`
3. `prompt_generator.py` calls backend at `http://127.0.0.1:5000/v1/chat/completions`
4. Backend (`app.py`) calls Gemini API
5. Gemini returns JSON array of variations
6. Frontend displays variations with copy/test buttons

## Setup & Run

**Terminal 1: Start Backend**
```powershell
cd c:\Users\swintern\gemini-adapter
.\.venv\Scripts\Activate.ps1
python app.py
```
Expected: `Running on http://127.0.0.1:5000`

**Terminal 2: Start Frontend**
```powershell
cd c:\Users\swintern\gemini-adapter
.\.venv\Scripts\Activate.ps1
python prompt_generator.py
```
Expected: `Running on http://127.0.0.1:3001`

**Open Browser:**
```
http://127.0.0.1:3001
```

## Configuration

### Change Gemini Model
Edit `app.py` line with:
```python
client.models.generate_content(model="gemini-2.0-flash", ...)
```

Available models:
- `gemini-2.0-flash` (recommended)
- `gemini-2.5-flash` (faster)
- `gemini-2.5-pro` (more powerful)

### Change Ports
- Backend: Edit `app.py` last line: `app.run(port=5000, ...)`
- Frontend: Edit `prompt_generator.py` last line: `app.run(port=3001, ...)`

## API Reference

### Generate Variations
```
POST http://127.0.0.1:5000/v1/chat/completions

Request:
{
  "prompt": "Your base prompt here",
  "variations": 5
}

Response:
{
  "variations": [
    "Optimized prompt 1...",
    "Optimized prompt 2...",
    ...
  ]
}
```

### Test Prompt (Frontend)
```
POST http://127.0.0.1:3001/api/test-prompt

Request:
{
  "prompt": "Your prompt to test"
}

Response:
{
  "response": "Gemini's response..."
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" on port 5000 | Start backend: `python app.py` |
| "Connection refused" on port 3001 | Start frontend: `python prompt_generator.py` |
| API key error | Check `AIzaSyCaVWsVYkMFCFbcer5bo2OCUr6f6bu8_xU` in `app.py` |
| No variations generated | Check Gemini API quota/limits |
| Slow response | Gemini API may be rate-limited; wait a few seconds |

## File Structure
```
gemini-adapter/
├── app.py                    # Backend API (Gemini)
├── prompt_generator.py       # Frontend server
├── prompt_generator.html     # Web UI
├── fix_app.py               # (Unused)
├── PROJECT.md               # This file
├── README.md                # User guide
├── AGENTS.md                # Agent workspace config
├── IDENTITY.md              # Agent identity
├── SOUL.md                  # Agent personality
├── USER.md                  # User preferences
├── TOOLS.md                 # Custom tools
├── HEARTBEAT.md             # Heartbeat checks
└── state/                   # (Empty state directory)
```

## Notes

- Both servers must be running simultaneously
- Frontend depends on backend being available
- Gemini API key is hardcoded in `app.py` (consider using environment variables)
- HTML/CSS/JS is embedded in `prompt_generator.html`
