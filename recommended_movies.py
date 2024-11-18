import streamlit as st
import pandas as pd

# Load Data
clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies.csv")  # Assuming a generic movies file for details

def get_recommended_movies(user_id):
    # Placeholder for recommendation logic
    cluster_recommendations = {
        cluster: list(movies_df.sample(6)['id'])
        for cluster in clustered_df['cluster'].unique()
    }
    return cluster_recommendations

def show():
    st.header("Recommended Movies for You")
    user_id = st.session_state.get("user_id", None)
    
    if user_id:
        recommendations = get_recommended_movies(user_id)
        st.write("Here are your recommended movies:")
        st.json(recommendations)
    else:
        st.write("Please go back to the home page to select a User ID.")
