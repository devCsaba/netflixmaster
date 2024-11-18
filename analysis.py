import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import plotly.express as px
import numpy as np

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
        all_genres = sorted(set(genre.lower() for genres in movies_df['genres'].dropna() for genre in genres.split(', ')))
        genre_matrix = np.array([[genres_counter.get(genre, 0) for genre in all_genres]])

        fig, ax = plt.subplots(figsize=(15, 3))
        sns.heatmap(genre_matrix, annot=True, fmt='.0f', cmap='Blues', xticklabels=all_genres, yticklabels=False, cbar_kws={'label': 'Frequency'})
        plt.xticks(rotation=45, ha='right')
        plt.title("Genre Frequency Distribution in Cluster")
        st.pyplot(fig)

        st.write("### Cluster Consistency Metric")
        if len(cluster_df) > 1:
            keyword_sets = [set(keywords.split(', ')) for keywords in cluster_df['keywords'].dropna()]
            total_pairs = 0
            total_overlap = 0

            for i in range(len(keyword_sets)):
                for j in range(i + 1, len(keyword_sets)):
                    overlap = len(keyword_sets[i].intersection(keyword_sets[j]))
                    total_overlap += overlap
                    total_pairs += 1

            avg_overlap = total_overlap / total_pairs if total_pairs > 0 else 0
            st.write(f"Average Keyword Overlap Between Movies in Cluster: {avg_overlap:.2f}")
        else:
            st.write("Not enough movies in this cluster to calculate consistency metric.")
