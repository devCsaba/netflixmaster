import streamlit as st
import pandas as pd
import json
from PGRS import PGRS

clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies2.csv")
pgrs = PGRS()

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
    #recommendations = sample_user_recommendations.get(int(user_id), {})
    #movie_ids = [movie_id for cluster in recommendations.values() for movie_id in cluster]

    movie_ids = parse_user_watch_history(user_id)
    movie_details = movies_df[movies_df['id'].isin(movie_ids)][['title', 'vote_average', 'genres', 'imdb_id', 'poster_path']]
    movie_details = movie_details.to_dict(orient='records')
    return movie_details, movie_ids


def display_movie_details(movie_details):
    if movie_details:
        for movie in movie_details:
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


def parse_recommendation_results(pgrs_result):

    for category, recomended_ids in pgrs_result.items():
        #st.write("================================================")
        movie_details = movies_df[movies_df['id'].isin(recomended_ids)][['title', 'vote_average', 'genres', 'imdb_id', 'poster_path']]
        movie_details = movie_details.to_dict(orient='records')
        display_movie_details(movie_details)


def show():
    user_id = st.session_state.get("user_id", None)
    
    if user_id:
        watch_history, watch_history_ids = get_user_watch_history(user_id)

        st.divider()
        st.subheader(f"Recomendations for user ID: {user_id} based on watch history")
        pgrs_result = pgrs.recommend_on_watch_history(watch_history_ids)
        parse_recommendation_results(pgrs_result)
        for category, recomended_ids in pgrs_result.items():
            print(f"{category} - {[pgrs.get_movie_title(movie_id) for movie_id in recomended_ids]}")

    else:
        st.write("Please choose user ID from side bar (it simulates user login)")


