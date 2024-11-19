import streamlit as st
import pandas as pd
from PGRS import PGRS

clustered_df = pd.read_csv("clustered_data_v2.csv")
movies_df = pd.read_csv("movies2.csv")
pgrs = PGRS()

if 'watched_movies_ids' not in st.session_state:
    st.session_state.watched_movies_ids = []


def get_movie_details(movie_ids):
    movie_details = movies_df[movies_df['id'].isin(movie_ids)][['title', 'vote_average', 'genres', 'imdb_id', 'poster_path']]
    movie_details = movie_details.to_dict(orient='records')
    return movie_details


def display_movie_details(movie_details):
    if movie_details:
        for movie in movie_details:
            cols = st.columns([1, 4]) 

            with cols[0]:
                poster_url = "https://image.tmdb.org/t/p/original" + str(movie["poster_path"])
                st.image(poster_url, width=80)
            
            with cols[1]:
                st.markdown(
                    f"""
                    **[{movie['title']}](https://www.imdb.com/title/{movie['imdb_id']})**   
                    *Rating:* {movie['vote_average']}  
                    *Genres:* {movie['genres']}
                    """
                )


def search_similar_movies(movie_title):
    found_movies = movies_df[movies_df['title'].str.contains(movie_title, case=False)]
    found_movies = found_movies[["id", "title"]]
    return found_movies


def show():
    st.header("Find Similar Movies")

    if st.button("Reset Movies Mix"):
        st.session_state.watched_movies_ids = []
        st.rerun()

    movie_title = st.text_input("Enter Movie Title (eng):")

    if len(movie_title) < 3:
        st.markdown("**Please, try input 3 or more characters**")

    col1, col2, col3 = st.columns([2, 3, 3])
    if movie_title:
        found_movies = search_similar_movies(movie_title)
        if not found_movies.empty:
            col1.markdown("**Movies found**")
            for _, movie in found_movies.iterrows():
                with col1:
                    # Checkbox to add/remove movie from watched list
                    is_watched = movie['id'] in st.session_state.watched_movies_ids
                    add_to_watched = st.checkbox(
                        f"{movie['title']}",
                        label_visibility="visible", 
                        key=f"movie_{movie['id']}", 
                        value=is_watched
                    )
                    
                    # Update watched movies list based on checkbox
                    if add_to_watched and movie['id'] not in st.session_state.watched_movies_ids:
                        st.session_state.watched_movies_ids.append(movie['id'])
                    elif not add_to_watched and movie['id'] in st.session_state.watched_movies_ids:
                        st.session_state.watched_movies_ids.remove(movie['id'])

                    #st.write(f"{movie['title']}")
        else:
            st.markdown("**No movies found. Try different title**")


    movie_details = get_movie_details(st.session_state.watched_movies_ids)
    print(st.session_state.watched_movies_ids)
    with col2:
        if movie_details:
            st.markdown("**Your movie selection mix**")
            display_movie_details(movie_details)

    # make prediction if user selected mix
    pgrs_result = pgrs.recommend_on_watch_history(st.session_state.watched_movies_ids)

    with col3:
        if movie_details:
            st.markdown("**Recomendations based on selection mix**")
            recommended_movie_details = [get_movie_details(recommended_ids) for category, recommended_ids in pgrs_result.items()]
            print(recommended_movie_details)
            for _ in recommended_movie_details:
                display_movie_details(_)
