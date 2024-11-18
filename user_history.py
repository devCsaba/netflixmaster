import streamlit as st
import pandas as pd

# Load Data
user_history_df = pd.read_csv("data/users_history_v2.csv")
movies_df = pd.read_csv("data/movies.csv")  # Placeholder for movie details

def get_user_history(user_id):
    watched_movies = user_history_df[user_history_df['user_id'] == int(user_id)]
    history = movies_df[movies_df['id'].isin(watched_movies['movie_id'])]
    return history

def show():
    st.header("Your Watch History")
    user_id = st.session_state.get("user_id", None)
    
    if user_id:
        history = get_user_history(user_id)
        st.write("Here is your watch history:")
        st.write(history[['title', 'genres', 'vote_average']])
    else:
        st.write("Please go back to the home page to select a User ID.")
