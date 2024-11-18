import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import plotly.express as px

clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies.csv")

merged_df = clustered_df.merge(movies_df, on='id')

def show():
    st.title("Movie Cluster Analysis")
    st.write("Analyze clusters by genre and keyword frequencies.")

    cluster_options = sorted(merged_df['cluster'].unique())
    selected_cluster = st.selectbox("Select a Cluster:", ["Select a Cluster"] + list(cluster_options))
    cluster_id_input = st.text_input("Or enter a Cluster ID:")

    cluster_id = int(cluster_id_input) if cluster_id_input else (selected_cluster if selected_cluster != "Select a Cluster" else None)

    if cluster_id is not None:
        cluster_df = merged_df[merged_df['cluster'] == int(cluster_id)]

        st.write(f"**Movies in Cluster {cluster_id}:**")
        st.write(cluster_df[['title', 'genres', 'keywords']])

        st.write("### Top 10 Keywords in Cluster")
        keywords_list = [keyword for keywords in cluster_df['keywords'].dropna() for keyword in keywords.split(', ')]
        keywords_counter = Counter(keywords_list)
        common_keywords = keywords_counter.most_common(10)
        keywords, counts = zip(*common_keywords)
        keywords_df = pd.DataFrame({'Keywords': keywords, 'Frequency': counts})

        fig = px.bar(keywords_df, x='Frequency', y='Keywords', orientation='h', title="Top 10 Keywords", labels={"Frequency": "Frequency", "Keywords": "Keywords"})
        st.plotly_chart(fig)

        st.write("### Top 10 Genres in Cluster")
        genres_list = [genre for genres in cluster_df['genres'].dropna() for genre in genres.split(', ')]
        genres_counter = Counter(genres_list)
        common_genres = genres_counter.most_common(10)
        genres, genre_counts = zip(*common_genres)
        
        plt.figure(figsize=(10, 6))
        plt.barh(genres, genre_counts)
        plt.xlabel("Frequency")
        plt.title("Top 10 Genres in Cluster")
        st.pyplot(plt)

        st.write("### Genre Frequency Heatmap")
        genre_freq = Counter(genres_list)
        genre_df = pd.DataFrame.from_dict(genre_freq, orient='index', columns=['Frequency']).reindex(sorted(genre_freq.keys()))
        
        fig, ax = plt.subplots(figsize=(10, 1))
        sns.heatmap(genre_df.T, cmap="YlGnBu", annot=True, cbar=True, xticklabels=True, yticklabels=False)
        plt.title("Genre Frequency Distribution in Cluster")
        st.pyplot(fig)
