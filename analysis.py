import streamlit as st
import pandas as pd

   # analysis.py
# analysis.py
import pandas as pd
import re

def load_imdb_data():
    basics = pd.read_csv(
        "https://datasets.imdbws.com/title.basics.tsv.gz",
        sep="\t",
        compression="gzip",
        usecols=["tconst", "primaryTitle", "startYear", "titleType"],
        dtype=str,
    )

    ratings = pd.read_csv(
        "https://datasets.imdbws.com/title.ratings.tsv.gz",
        sep="\t",
        compression="gzip",
        dtype=str,
    )

    merged = basics.merge(ratings, on="tconst", how="inner")
    merged = merged[merged["titleType"] == "movie"]

    merged["numVotes"] = pd.to_numeric(merged["numVotes"], errors="coerce")
    merged["averageRating"] = pd.to_numeric(merged["averageRating"], errors="coerce")

    merged = merged.dropna(subset=["numVotes", "averageRating"])

    merged["normTitle"] = (
        merged["primaryTitle"]
        .str.lower()
        .str.replace(r"[^\w]", "", regex=True)
    )

    return merged

# -----------------------------
# Load IMDb ratings (RAM safe)
# -----------------------------
def load_imdb_ratings():
    return pd.read_csv(
        "https://datasets.imdbws.com/title.ratings.tsv.gz",
        sep="\t",
        compression="gzip",
        nrows=100_000
    )

imdb_ratings = load_imdb_ratings()

# -----------------------------
# IMDb rating fetch
# -----------------------------

import re

def normalize(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())

def get_imdb_rating(movie_name, movie_year=None):
    data = load_imdb_data()

    search = normalize(movie_name)
    data["normTitle"] = data["primaryTitle"].apply(normalize)


    # Only movies
    data = data[data["titleType"] == "movie"]
    data = data.sort_values("numVotes", ascending=False).head(300_000)


    # Exact normalized match
    matches = data[data["normTitle"] == search]

    # Optional year filter
    if movie_year and not matches.empty:
        year_matches = matches[matches["startYear"] == str(movie_year)]
        if not year_matches.empty:
            matches = year_matches

    # Fallback: contains match
    if matches.empty:
        matches = data[data["normTitle"].str.contains(search, na=False)]

    if matches.empty:
        return None, None

    # Pick most popular version
    matches["numVotes"] = matches["numVotes"].astype(int)
    best = matches.sort_values("numVotes", ascending=False).iloc[0]

    return float(best["averageRating"]), int(best["numVotes"])







# -----------------------------
# Rotten Tomatoes (simulated)
# -----------------------------
def analyze_rt_reviews():
    return 272, 28  # pos, neg

# -----------------------------
# Final verdict logic
# -----------------------------
def final_verdict(imdb_rating, imdb_votes, rt_pos, rt_neg):
    if imdb_rating is None or imdb_votes is None:
        return "Insufficient IMDb data", 0.0

    rt_total = rt_pos + rt_neg
    rt_score = rt_pos / rt_total if rt_total > 0 else 0

    score = (imdb_rating / 10) * 0.6 + rt_score * 0.4

    verdict = "Good Movie" if score >= 0.6 else "Average Movie"
    return verdict, round(score, 2)


