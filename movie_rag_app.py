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


# Format background
st.markdown(
    """
    <style>
    .stTextInput>div>input {
        background-color: #f0f0f0;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# Create UI
st.title("🎬🎥 Movie RAG System 🍿🎟️ ")
st.caption("An AI Chatbot designed to answer all your questions about movies!")


# Create side search bar
# https://docs.streamlit.io/develop/api-reference/layout/st.sidebar
with st.sidebar:
    st.sidebar.title("🚨 Movies Avaliable in Database 🚨")
    title_query = st.text_input("Search for a movie title 🔻:")
    num_movies = st.slider("How many movies to retrieve?", 1, 10) # https://docs.streamlit.io/develop/api-reference/widgets/st.slider
    if st.button("Find Movie"): 
        if title_query:
            st.write(f"Results for \"{title_query}\" in Database:")
            retrieved_movies = find_movies(title_query, movie_titles, embedding_model, top_k=num_movies)
            for i, movie in enumerate(retrieved_movies, start=1):
                st.write(f"{i}. {movie}")

# Initialize chat history
# https://github.com/streamlit/llm-examples/blob/main/Chatbot.py
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
# Chat Interface: https://docs.streamlit.io/develop/api-reference/chat/st.chat_input
query = st.text_input("Enter your query:", "")

if st.button("Get Answer"):
    if query:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(query)

        # Add user message to chat history for immediate display
        st.session_state.messages.append({"role": "user", "content": query})
        # Show spinner widget while response is being generated
        with st.spinner("Generating Answer... Please Be Patient"):
            try:
                # Call the RAG pipeline function here
                #answer = rag_pipeline(query, collection, embedding_model, model, tokenizer, top_k=5)
                #st.write(textwrap.fill(answer, width=80))
                answer = "Hellooo Worldddd"
                pass
            except Exception as e:
                st.write("Error running query: {e}")
                answer = "Sorry I ran into a unexpected error, please try again!"

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer)

         # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        st.write("Please enter a query.")

    # https://streamlit.io/playground
    # https://streamlit.io/gallery?category=llms