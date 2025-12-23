
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
        usecols=["tconst", "primaryTitle", "startYear", "titleType"],
        dtype=str,
        nrows=1_500_000
    )

    ratings = pd.read_csv(
        "https://datasets.imdbws.com/title.ratings.tsv.gz",
        sep="\t",
        compression="gzip",
        dtype=str,
        nrows=1_500_000
    )

    merged = basics.merge(ratings, on="tconst", how="inner")

    # Keep only movies
    merged = merged[merged["titleType"] == "movie"]

    # Clean numeric fields
    merged["numVotes"] = pd.to_numeric(merged["numVotes"], errors="coerce")
    merged["averageRating"] = pd.to_numeric(merged["averageRating"], errors="coerce")

    merged = merged.dropna(subset=["numVotes", "averageRating"])

    # Normalize titles
    merged["normTitle"] = merged["primaryTitle"].apply(normalize_title)
    search = normalize_title(movie_name)

    # STEP 1: Exact title match
    candidates = merged[merged["normTitle"] == search]

    # STEP 2: If year exists, try filtering — but DO NOT force it
    if movie_year and not candidates.empty:
        year_matches = candidates[candidates["startYear"] == str(movie_year)]
        if not year_matches.empty:
            candidates = year_matches

    # STEP 3: If still empty, fallback to contains
    if candidates.empty:
        candidates = merged[merged["normTitle"].str.contains(search, na=False)]

    if candidates.empty:
        return None, None

    # STEP 4: Trust the most popular version
    best = candidates.sort_values("numVotes", ascending=False).iloc[0]

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

