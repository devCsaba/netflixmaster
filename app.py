import streamlit as st

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
    from pages import recommended_movies
    recommended_movies.show()

elif page == "Your History":
    from pages import user_history
    user_history.show()

elif page == "Movie Search":
    from pages import movie_search
    movie_search.show()

elif page == "Analysis":
    from pages import analysis
    analysis.show()
