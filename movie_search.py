import streamlit as st
import pandas as pd

# Load Data
clustered_df = pd.read_csv("data/clustered_data_v2.csv")
movies_df = pd.read_csv("data/movies.csv")

def find_similar_movies(movie_title):
    selected_movie = movies_df[movies_df['title'].str.contains(movie_title, case=False)]
    
    if not selected_movie.empty:
        cluster_id = clustered_df[clustered_df['id'] == selected_movie.iloc[0]['id']]['cluster'].values[0]
        similar_movies = clustered_df[clustered_df['cluster'] == cluster_id]
        similar_movie_ids = similar_movies['id'].sample(5).tolist()
        
        return movies_df[movies_df['id'].isin(similar_movie_ids)]
    else:
        return pd.DataFrame(columns=['title', 'genres', 'vote_average'])

def show():
    st.header("Find Similar Movies")
    movie_title = st.text_input("Enter a Movie Title:")
    
    if movie_title:
        similar_movies = find_similar_movies(movie_title)
        if not similar_movies.empty:
            st.write("Here are some movies similar to your search:")
            st.write(similar_movies[['title', 'genres', 'vote_average']])
        else:
            st.write("No similar movies found.")
