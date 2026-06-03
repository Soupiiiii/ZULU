"""
ZULU Computer Control — open apps and search the web
"""

import subprocess
import sys
import webbrowser
import urllib.parse


def open_app(app_name: str):
    """Open an application by name."""
    system = sys.platform

    try:
        if system == "darwin":  # macOS
            subprocess.Popen(["open", "-a", app_name])
        elif system == "win32":  # Windows
            subprocess.Popen(["start", app_name], shell=True)
        else:  # Linux
            subprocess.Popen([app_name.lower()])
    except Exception as e:
        print(f"[Could not open {app_name}: {e}]")


def search_web(query: str, engine: str = "google"):
    """Open a web search in the default browser."""
    engines = {
        "google": "https://www.google.com/search?q=",
        "bing": "https://www.bing.com/search?q=",
        "duckduckgo": "https://duckduckgo.com/?q=",
    }
    base_url = engines.get(engine, engines["google"])
    url = base_url + urllib.parse.quote_plus(query)
    webbrowser.open(url)


def get_system_info() -> dict:
    """Return basic system information."""
    import platform
    return {
        "os": platform.system(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python": sys.version,
    }
