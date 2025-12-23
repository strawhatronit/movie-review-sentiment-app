import streamlit as st
from analysis import get_imdb_rating, analyze_sentiment, final_verdict

st.set_page_config(
    page_title="Movie Review Sentiment Analyzer",
    layout="centered"
)

st.title("🎬 Movie Review Sentiment Analyzer")

# ----------- INPUT SECTION -----------
st.header("🔍 Movie Input")
movie_name = st.text_input(
    "Enter movie name",
    placeholder="Example: Titanic"
)

# Sample lightweight reviews (RAM safe)
sample_reviews = [
    "Amazing movie with emotional depth",
    "Great performances and direction",
    "Visually stunning and memorable",
    "Classic cinema experience",
    "A bit long but worth watching"
]

if st.button("Analyze Movie"):
    imdb_rating, imdb_votes = get_imdb_rating(movie_name)

    if imdb_rating is None:
        st.error("Movie not found in IMDb dataset.")
    else:
        pos, neg = analyze_sentiment(sample_reviews)
        verdict, score, explanation = final_verdict(
            imdb_rating, imdb_votes, pos, neg
        )

        # ----------- DATA SECTION -----------
        st.header("📊 Ratings & Data")
        col1, col2 = st.columns(2)
        col1.metric("IMDb Rating", imdb_rating)
        col2.metric("IMDb Votes", imdb_votes)

        st.write("Positive Reviews:", pos)
        st.write("Negative Reviews:", neg)

        # ----------- VERDICT -----------
        st.header("🧠 Verdict")
        st.success(verdict)
        st.progress(score)

        # ----------- EXPLANATION -----------
        st.header("📝 Explanation")
        st.info(explanation)
