import streamlit as st
import pandas as pd
import ast

# Load CSV files
clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies.csv")

# Function to parse recommendations from `example_inputs_outputs.txt`
def parse_recommendations(file_path):
    recommendations = {}
    with open(file_path, 'r') as file:
        content = file.read().split("---------")
        
        for entry in content:
            try:
                # Only process entries that contain both "input:" and "output:"
                if "input:" in entry and "output:" in entry:
                    user_id_line = entry.split("input:")[1].split("\n")[1].strip("[] \n")
                    output_line = entry.split("output:")[1].strip().strip('=')
                    
                    # Split user IDs and convert to integers
                    user_ids = list(map(int, user_id_line.split(", ")))
                    
                    # Convert the output dictionary string to a Python dictionary
                    output_dict = ast.literal_eval(output_line)
                    
                    # Store each user ID with its corresponding recommendations
                    for user_id in user_ids:
                        recommendations[user_id] = output_dict
            except ValueError as e:
                st.write(f"Error processing entry: {entry}")
                st.write(f"ValueError: {e}")
            except SyntaxError as e:
                st.write(f"Error parsing output dictionary for entry: {entry}")
                st.write(f"SyntaxError: {e}")
    return recommendations

# Parse the recommendations from `example_inputs_outputs.txt`
recommendations_file = "example_inputs_outputs.txt"
user_recommendations = parse_recommendations(recommendations_file)

def get_recommended_movies(user_id):
    # Get the clusters and movie IDs recommended for the user
    recommendations = user_recommendations.get(int(user_id), {})

    # Map movie IDs to movie details
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
