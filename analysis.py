
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
def get_imdb_rating(movie_name):
    basics = pd.read_csv(
        "https://datasets.imdbws.com/title.basics.tsv.gz",
        sep="\t",
        compression="gzip",
        usecols=["tconst", "primaryTitle"],
        nrows=200_000
    )

    ratings = pd.read_csv(
        "https://datasets.imdbws.com/title.ratings.tsv.gz",
        sep="\t",
        compression="gzip",
        nrows=200_000
    )

    merged = basics.merge(ratings, on="tconst")

    match = merged[
        merged["primaryTitle"].str.lower() == movie_name.lower()
    ]

    if match.empty:
        return None, None

    row = match.iloc[0]
    return float(row["averageRating"]), int(row["numVotes"])


# -----------------------------
# Rotten Tomatoes (simulated)
# -----------------------------
def analyze_rt_reviews():
    return 272, 28  # pos, neg

# -----------------------------
# Final verdict logic
# -----------------------------
def final_verdict(imdb_rating, imdb_votes, rt_pos, rt_neg):
    score = (imdb_rating / 10) * 0.6 + (rt_pos / (rt_pos + rt_neg)) * 0.4
    verdict = "Good Movie" if score > 0.6 else "Average Movie"
    return verdict, round(score, 2)
