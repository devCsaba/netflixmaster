import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies.csv")

unique_clusters = sorted(clustered_df['cluster'].unique())

def show():
    st.header("Cluster Analysis")
    
    st.write("### Cluster Distribution")
    cluster_counts = clustered_df['cluster'].value_counts()
    st.bar_chart(cluster_counts)

    st.write("### Keyword Frequency Analysis")
    keywords_list = [keyword for keywords in movies_df['keywords'].dropna() for keyword in keywords.split(', ')]
    keywords_counter = Counter(keywords_list)
    common_keywords = keywords_counter.most_common(10)
    keywords, counts = zip(*common_keywords)
    
    plt.figure(figsize=(10, 6))
    plt.barh(keywords, counts)
    plt.xlabel("Frequency")
    plt.title("Top 10 Keywords in Movies")
    st.pyplot(plt)

    st.write("### Genre Frequency Analysis")
    genres_list = [genre for genres in movies_df['genres'].dropna() for genre in genres.split(', ')]
    genres_counter = Counter(genres_list)
    common_genres = genres_counter.most_common(10)
    genres, genre_counts = zip(*common_genres)
    
    plt.figure(figsize=(10, 6))
    plt.barh(genres, genre_counts)
    plt.xlabel("Frequency")
    plt.title("Top 10 Genres in Movies")
    st.pyplot(plt)

    st.write("### Cluster Correlation Heatmap")
    # Generate a pivot table or dummy correlation matrix based on available data
    cluster_pivot = pd.crosstab(index=clustered_df['cluster'], columns=clustered_df['cluster'])
    plt.figure(figsize=(12, 8))
    sns.heatmap(cluster_pivot, cmap="YlGnBu", annot=False, cbar=True)
    st.pyplot(plt)

    st.write("### Explore Movies in a Specific Cluster")
    selected_cluster = st.selectbox("Select a Cluster ID:", options=["Select a Cluster"] + list(unique_clusters))
    cluster_id_input = st.text_input("Or enter a Cluster ID:")

    cluster_id = int(cluster_id_input) if cluster_id_input else (selected_cluster if selected_cluster != "Select a Cluster" else None)

    if cluster_id is not None:
        movies_in_cluster = clustered_df[clustered_df['cluster'] == int(cluster_id)]
        movie_ids = movies_in_cluster['id'].tolist()
        movie_details = movies_df[movies_df['id'].isin(movie_ids)][['title', 'genres', 'vote_average']]
        
        st.write(f"Movies in Cluster {cluster_id}:")
        for _, movie in movie_details.iterrows():
            st.write(f"{movie['title']} (Genre: {movie['genres']}, Rating: {movie['vote_average']})")
