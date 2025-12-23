# app.py
import streamlit as st
from analysis import get_imdb_rating, analyze_rt_reviews, final_verdict

st.set_page_config(page_title="Movie Review Analyzer", layout="centered")

st.title("🎬 Movie Review Sentiment Analyzer")

# ---------------- INPUT ----------------
st.header("1️⃣ Movie Input")
movie_name = st.text_input("Enter movie name")
movie_year = st.number_input("Release year (recommended)", min_value=1900, max_value=2025, value=2022)


if movie_name:
    # ---------------- DATA ----------------
    st.header("2️⃣ Ratings & Review Data")

    imdb_rating, imdb_votes = get_imdb_rating(movie_name, movie_year)
    rt_pos, rt_neg = analyze_rt_reviews()

    st.metric("IMDb Rating", imdb_rating)
    st.metric("IMDb Votes", imdb_votes)
    st.metric("RT Positive Reviews", rt_pos)
    st.metric("RT Negative Reviews", rt_neg)

    # ---------------- VERDICT ----------------
    st.header("3️⃣ Final Verdict")

    verdict, score = final_verdict(imdb_rating, imdb_votes, rt_pos, rt_neg)
    st.success(f"Final Verdict: {verdict}")
    st.info(f"Confidence Score: {score}")

    # ---------------- EXPLANATION ----------------
    st.header("4️⃣ Explanation")

    explanation = (
        f"After analyzing IMDb ratings and Rotten Tomatoes audience sentiment, "
        f"the movie **{movie_name}** is considered a **{verdict.lower()}** "
        f"with a confidence score of **{score}**."
    )

    st.write(explanation)

