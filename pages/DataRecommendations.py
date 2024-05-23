import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Set page configuration
st.set_page_config(page_title="Movie Recommender System", page_icon="🎬", layout="wide")

st.image("fdLogo.png")

# Hide the Streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Title of the page
st.title("Movie Recommender System")

# Load sample data
# @st.cache
def load_data():
    # Sample movie dataset
    url = "https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv"
    movies = pd.read_csv(url)
    return movies

movies = load_data()

# Display the dataset
st.subheader("Movie Dataset")
st.write(movies.head())

# User input for movie recommendations
st.header("Get Movie Recommendations")
selected_movie = st.selectbox("Select a movie you like:", movies['title'].values)
num_recommendations = st.slider("Number of recommendations:", min_value=1, max_value=10, value=5)

# Build the recommendation model
# @st.cache
def build_model(movies):
    # Compute TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    movies['authors'] = movies['authors'].fillna('')
    tfidf_matrix = tfidf.fit_transform(movies['authors'])
    
    # Compute cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

cosine_sim = build_model(movies)

# Function to get recommendations
# @st.cache
def get_recommendations(title, cosine_sim, movies):
    # Get the index of the movie that matches the title
    idx = movies[movies['title'] == title].index[0]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return movies.iloc[movie_indices]

# Generate movie recommendations
recommended_movies = get_recommendations(selected_movie, cosine_sim, movies)

# Display the recommendations
st.subheader("Recommended Movies")
st.write(recommended_movies[['title', 'authors', 'average_rating']])
