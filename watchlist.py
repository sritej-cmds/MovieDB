import json
import os

WATCHLIST_FILE = "watchlist.json"


def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return []

    try:
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_watchlist(items):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(items, f, indent=2)


def add_to_watchlist(movie):
    items = load_watchlist()

    title = movie.get("title")
    if not title:
        return {"error": "invalid movie"}

    if title in items:
        return {"message": "already in watchlist", "watchlist": items}

    items.append(title)
    save_watchlist(items)
    return {"message": "added", "watchlist": items}


def get_watchlist():
    return load_watchlist()


def remove_from_watchlist(title):
    items = load_watchlist()

    if title in items:
        items.remove(title)
        save_watchlist(items)
        return {"message": "removed", "watchlist": items}

    return {"message": "not found", "watchlist": items}
