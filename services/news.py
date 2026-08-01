"""News lookup service for Jarvis."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote_plus
from xml.etree import ElementTree

import httpx


@dataclass(slots=True)
class NewsItem:
    """A short news headline and link."""

    title: str
    link: str
    published: str | None = None


class NewsService:
    """Fetch top headlines from Google News RSS."""

    async def top_headlines(self, topic: str, limit: int = 5) -> list[NewsItem]:
        """Return recent headlines for a topic."""

        rss_url = f"https://news.google.com/rss/search?q={quote_plus(topic)}&hl=en-IN&gl=IN&ceid=IN:en"
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            response = await client.get(rss_url)
            response.raise_for_status()

        root = ElementTree.fromstring(response.text)
        items: list[NewsItem] = []
        for item in root.findall(".//item")[:limit]:
            title = item.findtext("title", default="Untitled")
            link = item.findtext("link", default="")
            published = item.findtext("pubDate")
            items.append(NewsItem(title=title, link=link, published=published))
        return items
