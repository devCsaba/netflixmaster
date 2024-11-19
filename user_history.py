import streamlit as st
import pandas as pd
import json

clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies2.csv")

def parse_user_watch_history(user_id):
    try:
        with open('users_history_v2.json', 'r') as file:
            data = json.load(file)
        
        for user in data:
            if user['user_id'] == user_id:
                return user.get('watched_movies', [])
        
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_user_watch_history(user_id):

    movie_ids = parse_user_watch_history(user_id)
    movie_details = movies_df[movies_df['id'].isin(movie_ids)][['title', 'vote_average', 'genres', 'imdb_id', 'poster_path']]
    movie_details = movie_details.to_dict(orient='records')
    return movie_details, movie_ids


def display_watch_history(watch_history):
    if watch_history:
        for movie in watch_history:
            cols = st.columns([1, 4]) 

            with cols[0]:
                poster_url = "https://image.tmdb.org/t/p/original" + str(movie["poster_path"])
                st.image(poster_url, width=80)
            
            with cols[1]:
                st.markdown(
                    f"""
                    **[{movie['title']}](https://www.imdb.com/title/{movie['imdb_id']})**   
                    *Rating:* {movie['vote_average']}  
                    *Genres:* {movie['genres']}
                    """
                )
    else:
        st.write("No watch history found.")


def show():
    user_id = st.session_state.get("user_id", None)
    
    if user_id:
        watch_history, watch_history_ids = get_user_watch_history(user_id)

        st.divider()
        st.subheader(f"Watch History (simulated) for user ID: {user_id}")
        display_watch_history(watch_history)
    else:
        st.write("Please choose user ID from side bar (it simulates user login)")

