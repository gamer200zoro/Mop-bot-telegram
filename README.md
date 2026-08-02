# Jarvis Telegram Super Bot

Jarvis is a modular Telegram bot built with Python 3.13+, `python-telegram-bot` v22+, FastAPI, SQLAlchemy async, and Supabase.

## What is working now

- Telegram commands for notes, todos, reminders, uploads, utilities, AI, PDFs, images, and timing tools
- FastAPI endpoints for `/`, `/health`, `/ping`, and `/metrics`
- Dashboard home, login, and admin overview pages
- Async SQLAlchemy database layer with Alembic migrations
- Supabase Storage integration for uploads
- Request logging, rate limiting, and exception handling
- CI smoke tests for imports, commands, dashboard, and core services

## Commands

Core commands currently include:

- `/start`, `/help`
- `/note`, `/notes`, `/todo`, `/todos`, `/remind`, `/reminders`
- `/timer`, `/stopwatch`, `/calendar`
- `/upload`, `/uploads`, `/download`
- `/weather`, `/news`, `/fx`, `/qr`
- `/ask`, `/summarize`, `/grammar`, `/translate`, `/explain`, `/ocr`, `/caption`
- `/pdfmerge`, `/pdfsplit`, `/imginfo`, `/imgconvert`, `/imgcompress`
- `/ban`, `/kick`, `/mute`, `/warn`

## Run locally

1. Copy `.env.example` to `.env`
2. Fill in the required values
3. Install dependencies
4. Start the app

```bash
python main.py
```

The web app starts even when `TELEGRAM_BOT_TOKEN` is missing. In that case, only the FastAPI side runs until the bot token is configured.

## Environment variables

Required for full functionality:

- `TELEGRAM_BOT_TOKEN`
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_STORAGE_BUCKET`
- `JWT_SECRET_KEY`
- `DASHBOARD_SECRET_KEY`
- `OPENAI_API_KEY` for AI features that call a provider
- `OPENAI_BASE_URL` and `OPENAI_MODEL` if you use a compatible provider

## Deployment

Jarvis is prepared for:

- Replit
- Docker
- Linux VPS

## Health checks

- `GET /health`
- `GET /ping`
- `GET /metrics`

## Notes

- The bot can run in polling mode for local development.
- The dashboard is intentionally lightweight now and can be expanded safely.
- Utilities that rely on external APIs will fail gracefully when their keys are missing.
