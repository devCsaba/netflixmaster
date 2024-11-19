import streamlit as st
import pandas as pd
import recommended_movies
import user_history
import movie_search
import analysis

st.set_page_config(layout="wide")
st.title("Movie Recommendation System")

user_history_df = pd.read_csv("users_history_v2.csv")
unique_user_ids = sorted(user_history_df['user_id'].unique())  # Get unique user IDs

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

st.sidebar.title("User Selection")

selected_id = st.sidebar.selectbox("Select a User ID:", options=["Select a User ID"] + list(unique_user_ids), index=0)

user_id_input = st.sidebar.text_input("Or enter User ID:")

if selected_id != "Select a User ID":
    st.session_state["user_id"] = selected_id
elif user_id_input:
    st.session_state["user_id"] = user_id_input

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "User History", "User Recommendations", "Movie Search"])

if page == "Home":
    st.write("Welcome to the Movie Recommendation System.")
    if st.session_state["user_id"]:
        st.write(f"Currently selected User ID: {st.session_state['user_id']}")
    else:
        st.write("Please enter or select your User ID in the sidebar to get personalized data.")

elif page == "User History":
    user_history.show()

elif page == "User Recommendations":
    recommended_movies.show()

elif page == "Movie Search":
    movie_search.show()

elif page == "Analysis":
    analysis.show()
