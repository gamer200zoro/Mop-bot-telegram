import asyncio
import threading
from contextlib import suppress

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application

from fastapi import FastAPI

from Jarvis.config.settings import settings
from Jarvis.database.database import init_db

# Placeholder imports for now, will be implemented later
# from api.app import app as fastapi_app
# from bot.client import build_telegram_application
# from scheduler.service import build_scheduler
# from utils.logging import configure_logging, get_logger

# Initialize FastAPI app
app = FastAPI(title="Jarvis Telegram Super Bot", description="Backend for Jarvis Telegram Bot and Dashboard")

# Initialize Telegram Bot Application
telegram_application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

async def start_command(update, context):
    await update.message.reply_text("Hello! I am Jarvis, your personal assistant bot.")

telegram_application.add_handler(CommandHandler("start", start_command))

@app.on_event("startup")
async def startup_event():
    await init_db()
    print("Database initialized.")

@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Simplified main function for now, will be expanded later
async def main() -> None:
    print("Starting Jarvis Telegram Super Bot...")

    # Run FastAPI in a separate thread
    # config = uvicorn.Config(app, host=settings.HOST, port=settings.PORT, log_level=settings.LOG_LEVEL.lower(), loop="asyncio", lifespan="on")
    # server = uvicorn.Server(config)
    # web_thread = threading.Thread(target=asyncio.run, args=(server.serve(),), daemon=True)
    # web_thread.start()

    # Run Telegram bot polling
    await telegram_application.initialize()
    await telegram_application.start()
    await telegram_application.updater.start_polling(drop_pending_updates=True)
    print("Telegram bot started.")

    try:
        # Keep the main thread alive
        while True:
            await asyncio.sleep(3600) # Sleep for an hour
    except KeyboardInterrupt:
        print("Stopping bot...")
        await telegram_application.updater.stop()
        await telegram_application.stop()
        await telegram_application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
