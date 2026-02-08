import streamlit as st
import pickle
import pandas as pd
import requests
import time

st.set_page_config(page_title="Movie Recommender", layout="wide")



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
st.caption("AI-based movie recommender system")

st.divider()

st.subheader("🔍 Search Movie")

search_text = st.text_input("Type movie name...", placeholder="e.g. Inception, Avatar, Titanic")

if search_text:
    filtered_movies = movies[movies["title"].str.contains(search_text, case=False, na=False)]
else:
    filtered_movies = pd.DataFrame(columns=["title"])

if not filtered_movies.empty:
    selected_movie_name = st.selectbox(
        "Select a movie:",
        filtered_movies["title"].values
    )
else:
    selected_movie_name = None
    st.info("Start typing to search movies...")

st.divider()

if selected_movie_name and st.button("🎯 Recommend Movie"):
    with st.spinner("Finding best recommendations..."):
        time.sleep(1)

    names, posters = recommend(selected_movie_name)

    if names:
        st.subheader("✨ Recommended Movies")

        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.image(poster, use_container_width=True)
                st.caption(name)
    else:
        st.warning("No recommendations found.")



st.divider()
st.caption("Created by Suraj Patil |  Movie Recommendation System")
