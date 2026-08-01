"""Administrative dashboard routes for Jarvis."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import SessionDep, get_current_subject
from database.models import LogEntry, Note, Reminder, Todo, Upload, User

router = APIRouter(prefix="/dashboard/admin", tags=["dashboard", "admin"])


@router.get("", response_class=HTMLResponse)
async def admin_overview(
    session: SessionDep,
    subject: str = Depends(get_current_subject),
) -> str:
    """Render a lightweight admin overview page with live entity counts."""

    counts = {
        "users": await session.scalar(select(func.count()).select_from(User)) or 0,
        "notes": await session.scalar(select(func.count()).select_from(Note)) or 0,
        "todos": await session.scalar(select(func.count()).select_from(Todo)) or 0,
        "reminders": await session.scalar(select(func.count()).select_from(Reminder)) or 0,
        "uploads": await session.scalar(select(func.count()).select_from(Upload)) or 0,
        "logs": await session.scalar(select(func.count()).select_from(LogEntry)) or 0,
    }

    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Jarvis Admin</title>
        <style>
          :root {{ color-scheme: dark; }}
          body {{ margin: 0; font-family: system-ui, sans-serif; background: #020617; color: #e2e8f0; }}
          .wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px; }}
          .hero {{ display: grid; gap: 10px; padding: 28px; background: #0f172a; border: 1px solid #334155; border-radius: 20px; }}
          .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-top: 20px; }}
          .card {{ padding: 18px; border-radius: 18px; background: #111827; border: 1px solid #334155; }}
          .muted {{ color: #94a3b8; }}
        </style>
      </head>
      <body>
        <div class="wrap">
          <section class="hero">
            <div class="muted">Signed in as {subject}</div>
            <h1 style="margin:0;">Admin overview</h1>
            <p style="margin:0;">Live counts from the database. No fluff, no smoke, just the numbers.</p>
          </section>
          <section class="grid">
            <div class="card"><div class="muted">Users</div><h2>{counts['users']}</h2></div>
            <div class="card"><div class="muted">Notes</div><h2>{counts['notes']}</h2></div>
            <div class="card"><div class="muted">Todos</div><h2>{counts['todos']}</h2></div>
            <div class="card"><div class="muted">Reminders</div><h2>{counts['reminders']}</h2></div>
            <div class="card"><div class="muted">Uploads</div><h2>{counts['uploads']}</h2></div>
            <div class="card"><div class="muted">Logs</div><h2>{counts['logs']}</h2></div>
          </section>
        </div>
      </body>
    </html>
    """
