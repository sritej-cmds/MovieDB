import requests
import time

TMDB_KEY = "YOUR_API_KEY" #upload your tmdb api key here
TMDB_BASE = "https://api.themoviedb.org/3"


def tmdb_get(endpoint, params=None, retries=3):
    params = params or {}
    params["api_key"] = TMDB_KEY
    url = f"{TMDB_BASE}/{endpoint}"

    for i in range(retries):
        try:
            res = requests.get(url, params=params, timeout=10)
            if res.status_code == 200:
                return res.json()
        except Exception:
            time.sleep(0.5 * (i + 1))

    return None


def get_movie_full(query):
    search = tmdb_get("search/movie", {"query": query})
    if not search or not search.get("results"):
        return {"error": "Movie not found"}

    movie_id = search["results"][0]["id"]

    details = tmdb_get(f"movie/{movie_id}")
    credits = tmdb_get(f"movie/{movie_id}/credits")

    if not details:
        return {"error": "Failed to fetch movie details"}

    actors = ""
    director = ""

    if credits:
        actors = ", ".join(
            c["name"] for c in credits.get("cast", [])[:5]
        )

        for c in credits.get("crew", []):
            if c.get("job") == "Director":
                director = c["name"]
                break

    return {
        "tmdb_id": movie_id,
        "title": details.get("title"),
        "overview": details.get("overview", ""),
        "poster": (
            f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}"
            if details.get("poster_path") else ""
        ),
        "genre": ", ".join(g["name"] for g in details.get("genres", [])),
        "rating": details.get("vote_average"),
        "release_date": details.get("release_date"),
        "runtime": f"{details.get('runtime')} min" if details.get("runtime") else "N/A",
        "actors": actors,
        "director": director
    }


def get_tmdb_recommendations(movie_id):
    res = tmdb_get(f"movie/{movie_id}/recommendations")
    return res.get("results", []) if res else []

