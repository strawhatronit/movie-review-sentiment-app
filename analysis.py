import pandas as pd
import re
import streamlit as st

@st.cache_data
def load_imdb_sample():
    # Load ONLY top movies by votes (RAM-safe)
    basics = pd.read_csv(
        "https://datasets.imdbws.com/title.basics.tsv.gz",
        sep="\t",
        compression="gzip",
        usecols=["tconst", "primaryTitle", "startYear", "titleType"],
        dtype=str,
        nrows=300_000
    )

    ratings = pd.read_csv(
        "https://datasets.imdbws.com/title.ratings.tsv.gz",
        sep="\t",
        compression="gzip",
        dtype=str,
        nrows=300_000
    )

    df = basics.merge(ratings, on="tconst")
    df = df[df["titleType"] == "movie"]

    df["numVotes"] = pd.to_numeric(df["numVotes"], errors="coerce")
    df["averageRating"] = pd.to_numeric(df["averageRating"], errors="coerce")
    df = df.dropna()

    df["normTitle"] = df["primaryTitle"].apply(
        lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
    )

    # Keep only popular movies
    df = df.sort_values("numVotes", ascending=False).head(100_000)

    return df


def get_imdb_rating(movie_name, movie_year=None):
    df = load_imdb_data()

    # Normalize search
    search = re.sub(r"[^a-z0-9]", "", movie_name.lower())
    df["normTitle"] = df["primaryTitle"].apply(
        lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
    )

    # Only movies
    df = df[df["titleType"] == "movie"]

    # Prioritize popular titles
    df = df.sort_values("numVotes", ascending=False).head(300_000)

    # Exact match
    matches = df[df["normTitle"] == search]

    # Year filter
    if movie_year and not matches.empty:
        year_matches = matches[matches["startYear"] == str(movie_year)]
        if not year_matches.empty:
            matches = year_matches

    # Fallback: contains
    if matches.empty:
        matches = df[df["normTitle"].str.contains(search, na=False)]

    if matches.empty:
        return None, None

    best = matches.iloc[0]
    return float(best["averageRating"]), int(best["numVotes"])





def analyze_rt_reviews():
    # Simulated Rotten Tomatoes
    return 272, 28


def final_verdict(imdb_rating, imdb_votes, rt_pos, rt_neg):
    if imdb_rating is None:
        return "Insufficient IMDb data", 0.0

    rt_total = rt_pos + rt_neg
    rt_score = rt_pos / rt_total if rt_total else 0

    score = (imdb_rating / 10) * 0.6 + rt_score * 0.4
    verdict = "Good Movie" if score >= 0.6 else "Average Movie"

    return verdict, round(score, 2)

