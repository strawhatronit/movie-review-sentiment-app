
   # analysis.py
# analysis.py
import pandas as pd

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
    basics = pd.read_csv(
        "https://datasets.imdbws.com/title.basics.tsv.gz",
        sep="\t",
        compression="gzip",
        usecols=["tconst", "primaryTitle", "startYear"],
        dtype=str,
        nrows=1_000_000
    )

    ratings = pd.read_csv(
        "https://datasets.imdbws.com/title.ratings.tsv.gz",
        sep="\t",
        compression="gzip",
        dtype=str,
        nrows=1_000_000
    )

    merged = basics.merge(ratings, on="tconst", how="inner")

    # Clean data
    merged = merged[merged["startYear"].str.isnumeric()]
    merged["startYear"] = merged["startYear"].astype(int)
    merged["numVotes"] = merged["numVotes"].astype(int)
    merged["averageRating"] = merged["averageRating"].astype(float)

    # Normalize titles
    merged["normTitle"] = merged["primaryTitle"].apply(normalize_title)
    search_title = normalize_title(movie_name)

    matches = merged[merged["normTitle"] == search_title]

    # Year filter (VERY IMPORTANT)
    if movie_year:
        matches = matches[matches["startYear"] == int(movie_year)]

    if matches.empty:
        return None, None

    # Pick the most trusted one
    best = matches.sort_values("numVotes", ascending=False).iloc[0]

    return best["averageRating"], best["numVotes"]





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

