import streamlit as st
import pandas as pd

   # analysis.py
# analysis.py
import pandas as pd
@st.cache_data(show_spinner="Loading IMDb datasets...")
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
def normalize_title(title):
    return (
        title.lower()
        .replace(" ", "")
        .replace(".", "")
        .replace("-", "")
    )

def get_imdb_rating(movie_name, movie_year=None):
    data = load_imdb_data()
    search = movie_name.lower().replace(" ", "").replace(".", "")

    matches = data[data["normTitle"] == search]

    if movie_year and not matches.empty:
        year_matches = matches[matches["startYear"] == str(movie_year)]
        if not year_matches.empty:
            matches = year_matches

    if matches.empty:
        matches = data[data["normTitle"].str.contains(search, na=False)]

    if matches.empty:
        return None, None

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
    # Safety check
    if imdb_rating is None or imdb_votes is None:
        return "Insufficient IMDb data", 0.0

    if rt_pos + rt_neg == 0:
        rt_score = 0
    else:
        rt_score = rt_pos / (rt_pos + rt_neg)

    score = (imdb_rating / 10) * 0.6 + rt_score * 0.4

    verdict = "Good Movie" if score >= 0.6 else "Bad Movie"
    return verdict, round(score, 2)

