import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies.csv")

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
