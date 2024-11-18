import streamlit as st
import recommended_movies
import user_history
import movie_search
import analysis

# App Title
st.title("Movie Recommendation System")

# Select User ID
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

st.sidebar.title("User Selection")
user_id = st.sidebar.text_input("Enter your User ID:")

# Set global user ID
if user_id:
    st.session_state["user_id"] = user_id

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Recommended Movies", "Your History", "Movie Search", "Analysis"])

# Page Routing
if page == "Home":
    st.write("Welcome to the Movie Recommendation System.")
    if st.session_state["user_id"]:
        st.write(f"Currently selected User ID: {st.session_state['user_id']}")
    else:
        st.write("Please enter your User ID in the sidebar to get personalized data.")

elif page == "Recommended Movies":
    recommended_movies.show()

elif page == "Your History":
    user_history.show()

elif page == "Movie Search":
    movie_search.show()

elif page == "Analysis":
    analysis.show()
