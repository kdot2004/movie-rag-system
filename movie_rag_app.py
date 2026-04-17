# Import dependencies
import streamlit as st # streamlit
import chromadb # Vector Store
from sentence_transformers import SentenceTransformer # Embedding model
import torch # LLM
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig # LLM
import textwrap # Answer generation
from movie_rag_pipeline import load_chromadb, load_embedding_model, load_llm_and_tokenizer # Loading models + vector store
from movie_rag_pipeline import rag_pipeline, find_movies, retrieve_documents  # Full pipeline
import time


# Load models and vector store
movie_chunks = load_chromadb(r"C:\Users\KRAyu\OneDrive\nlp_essentials\course_project\MovieSummaries\new_chroma_db\chroma_db", 
                             "movie_chunks")
movie_titles = load_chromadb(r"C:\Users\KRAyu\OneDrive\nlp_essentials\course_project\MovieSummaries\new_chroma_db\chroma_db", 
                             "movie_titles")
embedding_model = load_embedding_model("all-mpnet-base-v2")
#tokenizer, llm = load_llm_and_tokenizer("mistralai/Mistral-7B-Instruct-v0.3")


# Create UI
st.title("🎬🎥 Movie RAG System 🍿🎟️ ")
st.caption("An AI Chatbot designed to answer all your questions about movies! 🤖")


# Load movies
with open("movie_titles.txt", "r", encoding="utf-8") as f:
    movies = [line.strip() for line in f]
# Display avaliable movie data: https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox

# Store the initial value of widgets in session state
st.session_state.disabled = False

# Create side search bar
# https://docs.streamlit.io/develop/api-reference/layout/st.sidebar
with st.sidebar:
    st.sidebar.title("🚨 Movies Avaliable in Database 🚨")
    title_query = st.text_input("Search for a movie title:")
    num_movies = st.slider("How many movies to retrieve?", 1, 10) # https://docs.streamlit.io/develop/api-reference/widgets/st.slider
    if st.button("Find Movie"): 
        if title_query:
            st.write(f"Results for \"{title_query}\" in Database:")
            retrieved_movies = find_movies(title_query, movie_titles, embedding_model, top_k=num_movies)
            for i, movie in enumerate(retrieved_movies, start=1):
                st.write(f"{i}. {movie}")

col1, col2 = st.columns(2)
with col1:
    st.checkbox("Disable selectbox widget", key="disabled")
with col2:
    movie_options = st.selectbox(
                "Movies in Database 🔻",
                (movies)
            )
    disabled=st.session_state.disabled


# Chat Interface: https://docs.streamlit.io/develop/api-reference/chat/st.chat_input
query = st.text_input("Enter your query:", "")

if st.button("Get Answer"):
    with st.spinner("Generating Response...Please Wait"):
        if query:
                # Call the RAG pipeline function here
                #answer = rag_pipeline(query, collection, embedding_model, model, tokenizer, top_k=5)
                #st.write(textwrap.fill(answer, width=80))
                pass
    #else:
        #st.write("Please enter a query.")

# https://streamlit.io/playground
# https://streamlit.io/gallery?category=llms