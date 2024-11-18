import streamlit as st
import pandas as pd

clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies.csv")

sample_user_recommendations = {
    1: {
        0: [163814, 14891, 40353, 39282, 10002, 9074],
        1: [9388, 11910, 12110, 7010, 22292, 158916],
    },
    2: {
        0: [592230, 25598, 840, 426249, 52109, 450487],
        3: [866413, 14456, 215, 91979, 74725, 283995],
    },
    3: {
        2: [11246, 2289, 32008, 14638, 9306, 364708],
        4: [393561, 502425, 257440, 11795, 759054, 814800],
    }
}

def get_recommended_movies(user_id):
    recommendations = sample_user_recommendations.get(int(user_id), {})

    cluster_recommendations = {}
    for cluster, movie_ids in recommendations.items():
        movie_details = movies_df[movies_df['id'].isin(movie_ids)][['title', 'genres', 'vote_average']]
        cluster_recommendations[cluster] = movie_details.to_dict(orient='records')
    
    return cluster_recommendations

def show():
    st.header("Recommended Movies for You")
    user_id = st.session_state.get("user_id", None)
    
    if user_id:
        recommendations = get_recommended_movies(user_id)
        if recommendations:
            for cluster, movies in recommendations.items():
                st.subheader(f"Cluster {cluster}")
                st.write(movies)  # Display each cluster's list of movies
        else:
            st.write("No recommendations found for this user.")
    else:
        st.write("Please go back to the home page to select a User ID.")
