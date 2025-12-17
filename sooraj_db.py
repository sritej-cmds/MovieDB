from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(300), nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.Text)
    genre = db.Column(db.String(200))
    director = db.Column(db.String(200))
    actors_text = db.Column(db.Text)
    imdb_rating = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    ratings = db.relationship("Rating", backref="movie", lazy=True)
    comments = db.relationship("Comment", backref="movie", lazy=True)

    def avg_rating(self):
        if not self.ratings:
            return None
        return round(sum(r.score for r in self.ratings) / len(self.ratings), 2)

    def actors_list(self):
        if not self.actors_text:
            return []
        return [a.strip() for a in self.actors_text.split(",") if a.strip()]

    def to_dict(self):
        return {
            "id": self.id,
            "tmdb_id": self.tmdb_id,
            "title": self.title,
            "year": self.year,
            "description": self.description,
            "genre": self.genre,
            "director": self.director,
            "actors": self.actors_list(),
            "external_rating": self.imdb_rating,
            "avg_rating": self.avg_rating()
        }


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
