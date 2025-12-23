import pandas as pd
from textblob import TextBlob

ratings = pd.read_csv("title.ratings.tsv", sep="\t", dtype=str)
basics = pd.read_csv("title.basics.tsv", sep="\t", dtype=str)

def get_imdb_rating(movie_name):
    merged = basics.merge(ratings, on="tconst")
    match = merged[
        merged["primaryTitle"].str.lower() == movie_name.lower()
    ]
    if match.empty:
        return None, None
    row = match.iloc[0]
    return float(row["averageRating"]), int(row["numVotes"])

def analyze_sentiment(reviews):
    pos, neg = 0, 0
    for text in reviews:
        polarity = TextBlob(text).sentiment.polarity
        if polarity >= 0:
            pos += 1
        else:
            neg += 1
    return pos, neg

def final_verdict(imdb_rating, imdb_votes, pos, neg):
    score = pos / (pos + neg) if (pos + neg) else 0
    if imdb_rating >= 7 and score >= 0.6:
        verdict = "Good Movie"
    elif imdb_rating >= 5:
        verdict = "Average Movie"
    else:
        verdict = "Bad Movie"

    explanation = (
        f"Based on IMDb rating ({imdb_rating}) from {imdb_votes} votes "
        f"and audience sentiment ({pos} positive vs {neg} negative reviews), "
        f"the movie is classified as a {verdict.lower()}."
    )

    return verdict, round(score, 2), explanation
