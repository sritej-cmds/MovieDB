from flask import Flask, request, jsonify, send_from_directory
from search import search_movies
from sooraj_db import db, Movie, Rating, Comment
from external_api import (
    get_movie_full,
    get_tmdb_recommendations,
    tmdb_get
)
from watchlist import add_to_watchlist, get_watchlist, remove_from_watchlist

app = Flask(__name__)

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies_local.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()


# Frontend
@app.route("/ui")
def serve_ui():
    return send_from_directory("static", "index.html")


@app.route("/")
def home():
    return jsonify({"message": "Movie API is running"})


# Sync TMDB movie into local DB (needed for reviews/comments)
def sync_tmdb_to_local(data):
    movie = Movie.query.filter_by(tmdb_id=data["tmdb_id"]).first()
    if movie:
        return movie.id

    movie = Movie(
        tmdb_id=data["tmdb_id"],
        title=data["title"],
        year=int(data["release_date"].split("-")[0]) if data.get("release_date") else None,
        description=data.get("overview"),
        genre=data.get("genre", ""),
        director=data.get("director", ""),
        actors_text=data.get("actors", ""),
        imdb_rating=data.get("rating")
    )
    db.session.add(movie)
    db.session.commit()
    return movie.id


# Movie details
@app.route("/movie")
def movie_info():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "q parameter required"}), 400

    data = get_movie_full(query)
    if "error" in data:
        return jsonify(data), 404

    data["local_id"] = sync_tmdb_to_local(data)
    return jsonify(data)


# TMDB search (used for search bar)
@app.route("/search")
def search_route():
    return jsonify(
        search_movies(
            title=request.args.get("title"),
            genre=request.args.get("genre"),
            year=request.args.get("year", type=int),
            min_rating=request.args.get("rating", type=float)
        )
    )



# Recommendations
@app.route("/recommend")
def recommend():
    movie_id = request.args.get("id")
    if not movie_id:
        return jsonify({"error": "id required"}), 400

    return jsonify(get_tmdb_recommendations(movie_id))


# Watchlist (JSON-based)
@app.route("/watchlist/add", methods=["POST"])
def add_watch():
    title = request.json.get("title")
    movie = get_movie_full(title)

    if "error" in movie:
        return jsonify(movie), 404

    return jsonify(add_to_watchlist(movie))


@app.route("/watchlist")
def get_watch():
    return jsonify(get_watchlist())


@app.route("/watchlist/remove", methods=["POST"])
def remove_watch():
    title = request.json.get("title")
    return jsonify(remove_from_watchlist(title))


# Reviews
@app.route("/api/movies/<int:movie_id>/reviews", methods=["POST"])
def add_review(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "movie not found"}), 404

    data = request.json
    if not data.get("username") or not (1 <= int(data.get("score", 0)) <= 10):
        return jsonify({"error": "invalid input"}), 400

    review = Rating(
        username=data["username"],
        movie_id=movie_id,
        score=data["score"],
        review=data.get("review", "")
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({
        "message": "review added",
        "avg_rating": movie.avg_rating()
    })


@app.route("/api/movies/<int:movie_id>/reviews", methods=["GET"])
def list_reviews(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "movie not found"}), 404

    reviews = Rating.query.filter_by(movie_id=movie_id) \
        .order_by(Rating.created_at.desc()).all()

    return jsonify({
        "movie": movie.to_dict(),
        "reviews": [
            {
                "username": r.username,
                "score": r.score,
                "review": r.review,
                "created_at": r.created_at.isoformat()
            } for r in reviews
        ]
    })


# Comments
@app.route("/api/movies/<int:movie_id>/comments", methods=["POST"])
def add_comment(movie_id):
    if not Movie.query.get(movie_id):
        return jsonify({"error": "movie not found"}), 404

    data = request.json
    comment = Comment(
        username=data.get("username"),
        movie_id=movie_id,
        text=data.get("text")
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "comment added"})


@app.route("/api/movies/<int:movie_id>/comments", methods=["GET"])
def list_comments(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "movie not found"}), 404

    comments = Comment.query.filter_by(movie_id=movie_id) \
        .order_by(Comment.created_at.desc()).all()

    return jsonify({
        "movie": movie.to_dict(),
        "comments": [
            {
                "username": c.username,
                "text": c.text,
                "created_at": c.created_at.isoformat()
            } for c in comments
        ]
    })


if __name__ == "__main__":
    app.run(debug=True)
