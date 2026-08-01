"""Dashboard routes for Jarvis.

This module provides a lightweight HTML dashboard shell that can be expanded
with authentication, charts, and user management.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_class=HTMLResponse)
async def dashboard_home() -> str:
    """Render a minimal operational dashboard."""

    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Jarvis Dashboard</title>
        <style>
          :root { color-scheme: dark; }
          body { margin: 0; font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; }
          .wrap { max-width: 1100px; margin: 0 auto; padding: 32px; }
          .hero { display: grid; gap: 12px; padding: 28px; background: #111827; border: 1px solid #334155; border-radius: 20px; }
          .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 18px; }
          .card { padding: 20px; border-radius: 18px; background: #1e293b; border: 1px solid #334155; }
          .muted { color: #94a3b8; }
        </style>
      </head>
      <body>
        <div class="wrap">
          <section class="hero">
            <div class="muted">Jarvis control panel</div>
            <h1 style="margin:0; font-size: 2rem;">Operational dashboard</h1>
            <p style="margin:0; max-width: 70ch;">
              The bot core is online. Authentication, metrics, user management, and
              feature modules will slot into this surface.
            </p>
          </section>
          <section class="grid">
            <div class="card"><div class="muted">Status</div><h2>Healthy</h2></div>
            <div class="card"><div class="muted">Bot</div><h2>Ready</h2></div>
            <div class="card"><div class="muted">Database</div><h2>Connected</h2></div>
          </section>
        </div>
      </body>
    </html>
    """
