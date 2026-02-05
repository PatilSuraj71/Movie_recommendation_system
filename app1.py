import streamlit as st
import pickle
import pandas as pd
import requests
import time




def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=6f3b24f99ff347a4e020489593e0733e"
    )
    data = response.json()

    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommend_movies = []
    recommend_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]["id"]
        title = movies.iloc[i[0]]["title"]

        recommend_movies.append(title)
        recommend_movie_posters.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movie_posters
movies_dict = pickle.load(open("new_movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarities.pkl", "rb"))

st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies["title"].values
)

if st.button("Recommend Movie"):
    names, posters = recommend(selected_movie_name)

    if names:
        cols = st.columns(5)

        for col, name, poster in zip(cols, names, posters):
            with col:
                st.text(name)
                st.image(poster)
    else:
        st.warning("No recommendations found.")



with st.spinner("Loading recommendations..."):
    time.sleep(1.5)
st.success("Recommendations ready!")
