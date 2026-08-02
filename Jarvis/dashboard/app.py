from fastapi import FastAPI

dashboard_app = FastAPI(title="Jarvis Dashboard", description="Web dashboard for Jarvis Bot")

@dashboard_app.get("/")
async def read_root():
    return {"message": "Jarvis Dashboard is not yet implemented."}
