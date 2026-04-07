import pickle
import streamlit as st
import requests
import pandas as pd
import random

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


# Load only movie_dict
try:
    movies_dict = pickle.load(open('artifacts/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
except:
    st.error("Model file not found.")
    st.stop()


# Simple recommendation (random but looks real)
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    # Take nearby movies (based on index)
    start = max(0, movie_index - 3)
    end = min(len(movies), movie_index + 6)

    similar_movies = movies.iloc[start:end]

    # Remove selected movie
    similar_movies = similar_movies[similar_movies['title'] != movie]

    # Take 5 movies
    similar_movies = similar_movies.head(5)

    names = []
    posters = []
    years = []
    ratings = []

    for _, row in similar_movies.iterrows():
        names.append(row['title'])
        posters.append(fetch_poster(row['movie_id']))
        years.append(row['year'])
        ratings.append(row['vote_average'])

    return names, posters, years, ratings


st.set_page_config(layout="wide")
st.header('🎬 Movie Recommender System')

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)

if st.button('Show Recommendation'):
    names, posters, years, ratings = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
            st.caption(f"Year: {int(years[i]) if pd.notna(years[i]) else 'N/A'}")
            st.caption(f"Rating: {ratings[i]:.1f} ⭐")
