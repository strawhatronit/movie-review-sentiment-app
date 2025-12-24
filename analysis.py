import pandas as pd
import re

def load_imdb_data():
    return pd.read_csv("imdb_sample.csv")

def normalize(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())

def get_imdb_rating(movie_name, movie_year=None):
    df = load_imdb_data()

    df["normTitle"] = df["title"].apply(normalize)
    search = normalize(movie_name)

    matches = df[df["normTitle"] == search]

    if movie_year:
        year_matches = matches[matches["startYear"] == movie_year]
        if not year_matches.empty:
            matches = year_matches

    if matches.empty:
        return None, None

    best = matches.sort_values("numVotes", ascending=False).iloc[0]
    return float(best["averageRating"]), int(best["numVotes"])

def analyze_rt_reviews(movie_name, movie_year=None):
    import os

    BASE_DIR = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(BASE_DIR, "rt_sample.csv"))


    # normalize
    df["normTitle"] = df["title"].str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
    search = movie_name.lower().replace(" ", "").replace("-", "")

    matches = df[df["normTitle"] == search]

    if movie_year and not matches.empty:
        matches = matches[matches["year"] == movie_year]

    if matches.empty:
        return 0, 0

    row = matches.iloc[0]
    return int(row["rt_positive"]), int(row["rt_negative"])


def final_verdict(imdb_rating, imdb_votes, rt_pos, rt_neg):
    if imdb_rating is None:
        return "Insufficient IMDb data", 0.0

    rt_score = rt_pos / (rt_pos + rt_neg)
    score = (imdb_rating / 10) * 0.6 + rt_score * 0.4

    verdict = "Good Movie" if score >= 0.6 else "Average Movie"
    return verdict, round(score, 2)


