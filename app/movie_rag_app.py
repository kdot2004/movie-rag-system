"""
Movie RAG App via streamlit.

This script creates a UI for the Movie RAG Pipeline.
Users can type in several types of search queries.

The system expects plot, metadata, and character/actor
related questions. Additionally, users can ask for movie
recommendations.

This app is accompanied with a feature that allows users
to search for all the movies within the database. 
Asking questions of movies outside the database is unadvised.

Dependencies
------------
1. movie_rag_pipeline.py:
    - Ensure the file is under
    the same directory as the
    chroma collection and this
    app.
2. chromadb collections:
    - movie_chunks
    - movie_titles: 
        - run `movie_name_vectordb.py`
        - ensure movie_titles.txt
        and movie_title_embeddings.npy
        are under the same dir as the 
        chroma collection.
3. Nvida GPUs

**Note**
See requirements.txt to see what to install to run both this app
and the movie_rag_pipeline.
Run: pip install -r requirements.txt

Lastly note that certain feature are commented out. If you have the
approriate setup then feel free to comment out the llm/tokenizer as
well as the rag pipeline/answer under the try clause. 

Enjoy!
"""

# Import dependencies
import streamlit as st # streamlit
import chromadb # Vector Store
from sentence_transformers import SentenceTransformer # Embedding model
import torch # LLM
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig # LLM
import textwrap # Answer generation
from movie_rag_pipeline import (
    load_chromadb,
    load_embedding_model,
    load_llm_and_tokenizer,
    rag_pipeline,
    find_movies,
) # Loading models + vector store + pipeline

# Set page configuration https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
st.set_page_config(page_title="Movie RAG", page_icon="🎬", layout="wide")


# Load embedding model and vector store
movie_chunks = load_chromadb("/content/drive/MyDrive/chroma_db", "movie_chunks")
movie_titles = load_chromadb("/content/drive/MyDrive/chroma_db", "movie_titles")
embedding_model = load_embedding_model("all-mpnet-base-v2")


# Lazy loader for LLM
def get_llm():
    if "tokenizer" not in st.session_state or "mistral" not in st.session_state:
        with st.spinner("Loading language model for the first time..."):
            tokenizer, mistral = load_llm_and_tokenizer("mistralai/Mistral-7B-Instruct-v0.3")
            st.session_state.tokenizer = tokenizer
            st.session_state.mistral = mistral
    return st.session_state.tokenizer, st.session_state.mistral

# Create UI

# Title
st.title("🎬🎥 Movie RAG System 🍿🎟️ ")
st.caption("Note: the first question may take longer because the language model loads on first use.")

# Set up chat history
# https://mahapatra-preetam.medium.com/building-a-conversational-ai-with-memory-in-streamlit-using-langgraph-langchain-asyncio-and-96841a038fb5
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display a welcome message if the chat is empty
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write("Hello, I am your personal movie Q&A assistant! Ask away! 🤖")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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

# https://docs.streamlit.io/develop/api-reference/execution-flow/st.form
with st.form("qa_form"):
    query = st.text_input("Enter your query:") # Chat Interface: https://docs.streamlit.io/develop/api-reference/chat/st.chat_input
    ask_submit = st.form_submit_button("Get Answer")


if ask_submit:
    if query:
        # Add query to chat history
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Display
        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("Generating answer..."):
            try:
                tokenizer, mistral = get_llm() # Load LLM
                # Call pipeline
                answer = rag_pipeline(query, movie_chunks, embedding_model, mistral, tokenizer, top_k=5)
            except Exception as e:
                answer = f"Sorry, I ran into an error: {e}"
        # Add answer to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Print result
        with st.chat_message("assistant"):
            st.markdown(textwrap.fill(answer, width=80))
    else:
        st.warning("Please enter a query.")