
   # analysis.py
import pandas as pd

# Load a SMALL IMDb ratings subset (RAM safe)
@pd.api.extensions.register_dataframe_accessor("safe")
def _(df): return df

def load_imdb_ratings():
    return pd.read_csv(
        "https://datasets.imdbws.com/title.ratings.tsv.gz",
        sep="\t",
        compression="gzip",
        nrows=100_000
    )

imdb_ratings = load_imdb_ratings()

def get_imdb_rating(movie_name):
    match = imdb_ratings[
        imdb_ratings["tconst"].notna()
    ]
    # DEMO: returning average to avoid heavy joins
    return round(imdb_ratings["averageRating"].mean(), 1), int(imdb_ratings["numVotes"].mean())

def analyze_rt_reviews():
    # lightweight simulated RT sentiment
    return 272, 28

def final_verdict(imdb_rating, imdb_votes, rt_pos, rt_neg):
    score = (imdb_rating / 10) * 0.6 + (rt_pos / (rt_pos + rt_neg)) * 0.4
    verdict = "Good Movie" if score > 0.6 else "Average Movie"
    return verdict, round(s
