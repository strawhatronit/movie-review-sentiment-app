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

def analyze_rt_reviews():
    return 272, 28  # simulated

def final_verdict(imdb_rating, imdb_votes, rt_pos, rt_neg):
    if imdb_rating is None:
        return "Insufficient IMDb data", 0.0

    rt_score = rt_pos / (rt_pos + rt_neg)
    score = (imdb_rating / 10) * 0.6 + rt_score * 0.4

    verdict = "Good Movie" if score >= 0.6 else "Average Movie"
    return verdict, round(score, 2)


