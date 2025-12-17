MovieDB 

A simple movie exploration web app built using Flask + TMDB API, with support for searching movies, filtering by genre/rating/year, viewing details, adding reviews & comments, and maintaining a personal watchlist.

Features

 Movie Search

Search movies by title using TMDB

 Filters

Filter movies by genre, rating, and year

 Movie Details

Overview, genre, rating, director, cast, runtime

 Reviews

Add and view public 1–10 ratings

 Comments

Add short public comments for movies

 Watchlist

Add/remove movies to a local watchlist

 Recommendations

TMDB-based movie recommendations

Tech Stack

Backend: Python, Flask

Database: SQLite (SQLAlchemy)

Frontend: HTML, CSS, Vanilla JavaScript

API: TMDB (The Movie Database)

Project Structure
movieDBRefined/
│
├── app.py              # Main Flask app
├── external_api.py     # TMDB API integration
├── search.py           # Filter-based search (genre, rating, year)
├── sooraj_db.py        # Database models (movies, reviews, comments)
├── watchlist.py        # Watchlist logic
├── watchlist.json      # Stored watchlist
│
├── instance/
│   └── movies_local.db # SQLite database
│
├── static/
│   └── index.html      # Frontend UI
│
└── readme.txt

How to Run

Install dependencies:

pip install flask flask_sqlalchemy requests


Run the app:

python app.py


Open in browser:

http://127.0.0.1:5000/ui

Notes

This is a development project, not intended for production use.


TMDB API key is required in external_api.py.
