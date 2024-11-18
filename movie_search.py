import streamlit as st
import pandas as pd

clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies.csv")

all_movie_titles = movies_df['title'].sort_values().unique()

def find_similar_movies(movie_title):
    selected_movie = movies_df[movies_df['title'].str.contains(movie_title, case=False)]
    
    if not selected_movie.empty:
        cluster_id = clustered_df[clustered_df['id'] == selected_movie.iloc[0]['id']]['cluster'].values[0]
        
        similar_movies = clustered_df[clustered_df['cluster'] == cluster_id]
        similar_movie_ids = similar_movies['id'].sample(5).tolist()
        
        return movies_df[movies_df['id'].isin(similar_movie_ids)][['title', 'genres', 'vote_average']]
    else:
        return pd.DataFrame(columns=['title', 'genres', 'vote_average'])

def show():
    st.header("Find Similar Movies")
    
    selected_movie_title = st.selectbox("Select a Movie Title:", options=["Select a Movie"] + list(all_movie_titles))
    
    movie_title_input = st.text_input("Or enter a Movie Title:")

    movie_title = movie_title_input if movie_title_input else (selected_movie_title if selected_movie_title != "Select a Movie" else None)

    if movie_title:
        similar_movies = find_similar_movies(movie_title)
        if not similar_movies.empty:
            st.write("Here are some movies similar to your selection:")
            for _, movie in similar_movies.iterrows():
                st.write(f"{movie['title']} (Genre: {movie['genres']}, Rating: {movie['vote_average']})")
        else:
            st.write("No similar movies found.")
