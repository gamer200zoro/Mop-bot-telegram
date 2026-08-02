# Jarvis Usage Manual

## What Jarvis is

Jarvis is a Telegram super bot with a FastAPI backend, a dashboard, database storage, file tools, utilities, AI helpers, and moderation commands.

## Where to run it

Jarvis can run in any of these places:

- **Local machine** for development and testing
- **Replit** for quick hosted development
- **Docker** for a repeatable container setup
- **Linux VPS** for a stable long-running deployment

## Quick start

1. Copy `.env.example` to `.env`
2. Fill in the required values
3. Install dependencies
4. Start the bot

```bash
python main.py
```

## Required environment values

Set these for full functionality:

- `TELEGRAM_BOT_TOKEN`
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_STORAGE_BUCKET`
- `JWT_SECRET_KEY`
- `DASHBOARD_SECRET_KEY`

Optional but useful:

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `TELEGRAM_ADMIN_IDS`

## What happens when you run it

- FastAPI starts on the configured host and port
- The Telegram bot starts in polling mode when a token is present
- The dashboard becomes available on the web port
- The scheduler starts reminder delivery jobs

## Common commands

### Notes and todos

- `/note title | content`
- `/notes`
- `/todo title | priority`
- `/todos`

### Timing

- `/timer 10m reminder text`
- `/stopwatch start`
- `/stopwatch lap`
- `/stopwatch stop`
- `/calendar month year`

### Files

- Reply to a media message and use `/upload`
- `/uploads`
- `/download storage/path/file.ext`

### Utilities

- `/weather city name`
- `/news topic`
- `/fx amount from_currency to_currency`
- `/qr text or url`

### AI

- `/ask question`
- `/summarize text`
- `/grammar text`
- `/translate target_language text`
- `/explain code`
- Reply to an image and use `/ocr` or `/caption`

### Documents and images

- `/pdfmerge file_id_1 file_id_2 ...`
- Reply to a PDF and use `/pdfsplit start [end]`
- Reply to an image and use `/imginfo`
- Reply to an image and use `/imgconvert format`
- Reply to an image and use `/imgcompress [quality]`

### Moderation

- `/ban user_id`
- `/kick user_id`
- `/mute user_id`
- `/warn user_id [reason]`

## Dashboard access

Open the dashboard in a browser on the same host and port as FastAPI:

- `/dashboard`
- `/dashboard/login`
- `/dashboard/admin`

Use the dashboard secret from `DASHBOARD_SECRET_KEY` to log in.

## Troubleshooting

- If the bot does not start, check `TELEGRAM_BOT_TOKEN`
- If database features fail, check `DATABASE_URL`
- If uploads fail, check the Supabase storage settings
- If AI commands fail, verify `OPENAI_API_KEY` or expect local fallback behavior where supported
- If moderation commands do nothing, make sure your Telegram ID is listed in `TELEGRAM_ADMIN_IDS`
