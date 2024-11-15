#import streamlit as st

# Set page title and icon
#st.set_page_config(page_title="Under Construction", page_icon="🍲")

# Page content
#st.title("We are still cooking... 🍲")
#st.markdown("""
#Welcome to our page! This feature is currently under development.  
#Stay tuned for more updates as we continue to build and improve our app.

#In the meantime, feel free to explore other features or check back later!
#""")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

clustered_df = pd.read_csv("clustered_data.csv")
movies_df = pd.read_csv("movies.csv")

merged_df = clustered_df.merge(movies_df, on='id')

st.title("Movie Cluster Analysis by Keywords and Genres")
st.write("Evaluate the coherence of clusters based on keywords and genres.")

cluster_options = sorted(merged_df['cluster'].unique())
selected_cluster = st.selectbox("Select a Cluster:", cluster_options)

cluster_df = merged_df[merged_df['cluster'] == selected_cluster]

all_genres = sorted(set(genre for genres in cluster_df['genres'].dropna() for genre in genres.split(', ')))
selected_genre = st.multiselect("Filter by Genre:", all_genres)

if selected_genre:
    cluster_df = cluster_df[cluster_df['genres'].apply(lambda x: any(genre in x for genre in selected_genre))]
    
all_keywords = sorted(set(keyword for keywords in cluster_df['keywords'].dropna() for keyword in keywords.split(', ')))
selected_keyword = st.multiselect("Filter by Keyword:", all_keywords)

if selected_keyword:
    cluster_df = cluster_df[cluster_df['keywords'].apply(lambda x: any(keyword in x for keyword in selected_keyword))]

st.write(f"Movies in Cluster {selected_cluster} (Filtered by Selected Genres and Keywords):")
st.write(cluster_df[['title', 'genres', 'keywords']])

st.write("### Keyword Frequency in Cluster")
keywords_list = [keyword for keywords in cluster_df['keywords'].dropna() for keyword in keywords.split(', ')]
keywords_counter = Counter(keywords_list)
common_keywords = keywords_counter.most_common(10)
keywords, counts = zip(*common_keywords)

plt.figure(figsize=(10, 6))
plt.barh(keywords, counts)
plt.xlabel("Frequency")
plt.title("Top 10 Keywords in Cluster")
st.pyplot(plt)

st.write("### Genre Frequency in Cluster")
genres_list = [genre for genres in cluster_df['genres'].dropna() for genre in genres.split(', ')]
genres_counter = Counter(genres_list)
common_genres = genres_counter.most_common(10)
genres, genre_counts = zip(*common_genres)

plt.figure(figsize=(10, 6))
plt.barh(genres, genre_counts)
plt.xlabel("Frequency")
plt.title("Top 10 Genres in Cluster")
st.pyplot(plt)

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

