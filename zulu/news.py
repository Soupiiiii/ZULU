"""
ZULU News — fetches current world events via NewsAPI
"""

import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"


def get_news(country: str = "us", category: str = "general", page_size: int = 10) -> list[str]:
    """
    Fetch top headlines. Returns a list of headline strings.
    Get a free API key at https://newsapi.org
    """
    if not NEWS_API_KEY:
        return ["News API key not configured. Set the NEWS_API_KEY environment variable."]

    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "category": category,
        "pageSize": page_size,
    }

    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        headlines = []
        for a in articles:
            title = a.get("title", "")
            source = a.get("source", {}).get("name", "")
            if title and "[Removed]" not in title:
                headlines.append(f"{title} — {source}" if source else title)
        return headlines
    except requests.RequestException as e:
        return [f"Unable to fetch news: {e}"]


def get_world_news(page_size: int = 10) -> list[str]:
    """Fetch international top headlines."""
    if not NEWS_API_KEY:
        return ["News API key not configured."]

    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": page_size,
        "sortBy": "publishedAt",
    }

    try:
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={**params, "q": "world news"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        return [
            f"{a.get('title','')} — {a.get('source',{}).get('name','')}"
            for a in articles
            if a.get("title") and "[Removed]" not in a.get("title", "")
        ]
    except requests.RequestException as e:
        return [f"Unable to fetch world news: {e}"]
