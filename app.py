import pickle
import streamlit as st
import requests
import pandas as pd


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        pass
    return "https://placehold.co/500x750?text=No+Poster"


# Load data
try:
    movies_dict = pickle.load(open('artifacts/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
except:
    st.error("Model file not found.")
    st.stop()


movies = movies.head(1000)


# Simple similarity (no sklearn)
def simple_similarity(a, b):
    a_words = set(str(a).lower().split())
    b_words = set(str(b).lower().split())
    return len(a_words & b_words)


def recommend(movie):
    movie_row = movies[movies['title'] == movie].iloc[0]

    scores = []

    for i, row in movies.iterrows():
        score = simple_similarity(movie_row.get('tags', movie), row.get('tags', row['title']))
        scores.append((i, score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    names, posters, years, ratings = [], [], [], []

    for i, _ in scores[1:6]:
        row = movies.iloc[i]
        names.append(row['title'])
        posters.append(fetch_poster(row['movie_id']))
        years.append(row['year'])
        ratings.append(row['vote_average'])

    return names, posters, years, ratings


st.set_page_config(layout="wide")
st.header('🎬 Movie Recommender System')

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "🔍 Search and select a movie",
    movie_list
)

if st.button('Show Recommendation'):
    names, posters, years, ratings = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(len(names)):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
            st.caption(f"Year: {int(years[i]) if pd.notna(years[i]) else 'N/A'}")
            st.caption(f"Rating: {ratings[i]:.1f} ⭐")
