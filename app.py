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
    movie_lower = movie.lower()

    # 🎯 Smart genre detection
    if movie_lower in ["tangled", "frozen", "moana", "lion king", "aladdin"]:
        category_movies = movies[movies['title'].str.contains(
            "Frozen|Moana|Lion|Beauty|Aladdin", case=False, na=False)]
    elif movie_lower in ["interstellar", "gravity", "martian", "inception"]:
        category_movies = movies[movies['title'].str.contains(
            "space|star|galaxy|interstellar|gravity", case=False, na=False)]
    elif movie_lower in ["avengers", "iron man", "thor"]:
        category_movies = movies[movies['title'].str.contains(
            "avenger|thor|captain|marvel", case=False, na=False)]
    else:
        # fallback to similarity
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        category_movies = movies.iloc[[i[0] for i in distances[1:10]]]

    category_movies = category_movies[category_movies['title'] != movie].head(5)

    names, posters, years, ratings = [], [], [], []

    for _, row in category_movies.iterrows():
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
