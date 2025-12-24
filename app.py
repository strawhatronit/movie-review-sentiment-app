# app.py
import streamlit as st
from analysis import get_imdb_rating, analyze_rt_reviews, final_verdict

st.set_page_config(page_title="Movie Review Analyzer", layout="centered")

st.title("🎬 Movie Review Sentiment Analyzer")

st.header("1️⃣ Movie Input")
movie_name = st.text_input("Enter movie name")
movie_year = st.number_input(
    "Release year (recommended)",
    min_value=1900,
    max_value=2025,
    value=2022
)

if movie_name:
    st.header("2️⃣ Ratings & Review Data")

    imdb_rating, imdb_votes = get_imdb_rating(movie_name, movie_year)
    rt_pos, rt_neg = analyze_rt_reviews(movie_name, movie_year)


    st.metric("IMDb Rating", imdb_rating if imdb_rating else "N/A")
    st.metric("IMDb Votes", imdb_votes if imdb_votes else "N/A")
    st.metric("RT Positive Reviews", rt_pos)
    st.metric("RT Negative Reviews", rt_neg)

    st.header("3️⃣ Final Verdict")
    verdict, score = final_verdict(imdb_rating, imdb_votes, rt_pos, rt_neg)

    st.success(f"Final Verdict: {verdict}")
    st.info(f"Confidence Score: {score}")
    if imdb_rating is None:
       st.warning("Movie not found in IMDb sample dataset.")

