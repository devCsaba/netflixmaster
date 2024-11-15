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

# Load data
clustered_df = pd.read_csv("clustered_data.csv")
movies_df = pd.read_csv("movies.csv")

# Merge the two datasets on 'id' column
merged_df = clustered_df.merge(movies_df, on='id')

# Streamlit app layout
st.title("Movie Cluster Exploration")
st.write("Explore movies by clusters, genres, and keywords.")

# Cluster selection
cluster_options = sorted(merged_df['cluster'].unique())
selected_cluster = st.selectbox("Select a Cluster:", cluster_options)

# Filter by selected cluster
cluster_df = merged_df[merged_df['cluster'] == selected_cluster]

# Genre filter
all_genres = sorted(set(genre for genres in cluster_df['genres'].dropna() for genre in genres.split(', ')))
selected_genre = st.multiselect("Filter by Genre:", all_genres)

if selected_genre:
    cluster_df = cluster_df[cluster_df['genres'].apply(lambda x: any(genre in x for genre in selected_genre))]

# Keyword filter
all_keywords = sorted(set(keyword for keywords in cluster_df['keywords'].dropna() for keyword in keywords.split(', ')))
selected_keyword = st.multiselect("Filter by Keyword:", all_keywords)

if selected_keyword:
    cluster_df = cluster_df[cluster_df['keywords'].apply(lambda x: any(keyword in x for keyword in selected_keyword))]

# Display filtered movies
st.write(f"Movies in Cluster {selected_cluster}:")
st.write(cluster_df[['title', 'vote_average', 'genres', 'release_date', 'popularity']])

# Optional: Interactive chart with movie ratings and popularity
st.write("### Ratings vs. Popularity")
st.write("The chart below shows the distribution of ratings and popularity for movies in the selected cluster.")
st.vega_lite_chart(cluster_df, {
    "mark": "circle",
    "encoding": {
        "x": {"field": "vote_average", "type": "quantitative", "title": "Vote Average"},
        "y": {"field": "popularity", "type": "quantitative", "title": "Popularity"},
        "tooltip": [{"field": "title", "type": "nominal"}, {"field": "vote_average", "type": "quantitative"}, {"field": "popularity", "type": "quantitative"}]
    }
})
