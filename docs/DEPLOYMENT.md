# Jarvis Deployment Guide

## Local machine

Best for development, debugging, and fast iteration.

```bash
cp .env.example .env
pip install -r requirements.txt
python main.py
```

Open the API in a browser at the configured host and port. The bot uses polling when `TELEGRAM_BOT_TOKEN` is present.

## Replit

Use this when you want a quick online workspace.

1. Add the environment variables from `.env.example`
2. Install dependencies with the package manager or `pip`
3. Run `python main.py`
4. Keep the web endpoint active with a monitoring ping if needed

The app already includes a `replit.toml` file for the workspace setup.

## Docker

Use Docker when you want a clean repeatable runtime.

1. Build the image
2. Pass the environment variables into the container
3. Expose the configured HTTP port
4. Run the container

Typical flow:

```bash
docker build -t jarvis .
docker run --env-file .env -p 8000:8000 jarvis
```

## Linux VPS

Use a VPS when you want 24x7 availability.

1. Clone the repository
2. Install Python 3.13 and system dependencies
3. Create the virtual environment
4. Add your environment variables
5. Run `python main.py` under a process manager such as `systemd` or `tmux`

## Production checklist

Before exposing the bot to real users, confirm:

- `TELEGRAM_BOT_TOKEN` is set
- `DATABASE_URL` points to PostgreSQL or Supabase Postgres
- `SUPABASE_URL` and keys are valid
- `DASHBOARD_SECRET_KEY` and `JWT_SECRET_KEY` are strong and unique
- `OPENAI_API_KEY` is configured if you want cloud AI features
- The `/health` endpoint responds successfully
- The Telegram bot can send a test message

## UptimeRobot

Point UptimeRobot at the `/health` endpoint or `/ping` endpoint on the running FastAPI service.
