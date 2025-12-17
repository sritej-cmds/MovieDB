from external_api import tmdb_get

# TMDB genre name → ID mapping
GENRE_MAP = {
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "comedy": 35,
    "crime": 80,
    "drama": 18,
    "fantasy": 14,
    "horror": 27,
    "romance": 10749,
    "sci-fi": 878,
    "thriller": 53
}


def search_movies(
    title=None,
    genre=None,
    year=None,
    min_rating=None
):
    """
    Unified TMDB search:
    - title: movie name
    - genre: genre name (Action, Drama, etc.)
    - year: release year
    - min_rating: minimum TMDB rating
    """

    params = {
        "sort_by": "popularity.desc"
    }

    # Decide endpoint
    endpoint = "discover/movie"

    if title:
        endpoint = "search/movie"
        params["query"] = title

    if genre:
        genre_id = GENRE_MAP.get(genre.lower())
        if genre_id:
            params["with_genres"] = genre_id

    if year:
        params["year"] = year

    if min_rating:
        params["vote_average.gte"] = min_rating

    res = tmdb_get(endpoint, params)
    if not res or "results" not in res:
        return []

    movies = []

    for m in res["results"]:
        movies.append({
            "tmdb_id": m.get("id"),
            "title": m.get("title"),
            "year": (
                m.get("release_date", "").split("-")[0]
                if m.get("release_date") else None
            ),
            "overview": m.get("overview"),
            "poster": (
                f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}"
                if m.get("poster_path") else ""
            ),
            "rating": m.get("vote_average")
        })

    return movies
