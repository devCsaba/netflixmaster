import streamlit as st
import pandas as pd

clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies.csv")

def get_recommended_movies(user_id):
    cluster_recommendations = {
        int(cluster): [int(movie_id) for movie_id in movies_df.sample(6)['id']]
        for cluster in clustered_df['cluster'].unique()
    }
    return cluster_recommendations

def show():
    st.header("Recommended Movies for You")
    user_id = st.session_state.get("user_id", None)
    
    if user_id:
        recommendations = get_recommended_movies(user_id)
        st.write("Here are your recommended movies:")
        st.json(recommendations)  # Displaying as JSON for easy viewing
    else:
        st.write("Please go back to the home page to select a User ID.")
