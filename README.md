# Jarvis

Jarvis is a modular Telegram super bot built with Python 3.13+, python-telegram-bot v22+, FastAPI, SQLAlchemy async, and Supabase.

## What is in place

- Telegram bot entrypoint with `/start`
- FastAPI app with `/health`, `/ping`, and `/metrics`
- Async SQLAlchemy database layer
- Initial Alembic migration history
- Docker and Replit launch configuration
- Typed settings and structured logging

## Run locally

1. Copy `.env.example` to `.env`
2. Fill in the required secrets
3. Install dependencies
4. Start the app

```bash
python main.py
```

The web app starts even if the Telegram token is not configured. In that case, the bot remains disabled until `TELEGRAM_BOT_TOKEN` is set.

## Environment variables

Required for full functionality:

- `TELEGRAM_BOT_TOKEN`
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `JWT_SECRET_KEY`
- `DASHBOARD_SECRET_KEY`

## Deployment targets

- Replit
- Docker
- Linux VPS

## Health endpoints

- `GET /health`
- `GET /ping`
- `GET /metrics`

## Next layers

The next commits will expand moderation, notes, todos, reminders, dashboard auth, storage, AI services, file tools, and CI/CD.
