# 🎬 **Movie RAG System** 🎥
> 🚀 A Retrieval-Augmented Generation system for intelligent movie search and discovery.

---

## Table of Contents 
- [Overview](#-overview)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#️-usage)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Data Sources](#-data-sources)

---

## 📌 Overview
This project implements a Retrieval-Augmented Generation (RAG) system for answering movie-related questions.

It supports multiple query types, including:
- plot-based questions 
- actor and character lookups 
- metadata retrieval
- recommendation-style queries

Designed for movie fans, students, and developers seeking accurate, data-grounded film insights.

---

## 📸 Demo
![Movie RAG Query Demo 1](assets/query1.gif)
![Movie RAG Query Demo 3](assets/query3.gif)
[Movie RAG YT Link](https://youtu.be/107usbwWhow?si=lm6dqRxsn1LxVp0t)

---

## 📦 Installation
This project was run using Google Colab rather than a local Python environment. 
Because of this, a separate `requirements.txt` file was not included. 
All required libraries are installed directly inside the Colab notebook before the Streamlit app is launched.

The main setup steps include:

```
python
!pip install streamlit pyngrok chromadb sentence-transformers transformers accelerate bitsandbytes
```

---

## 🛠️ Usage
1. Store CMU data files locally 
- [Data Sources](#-data-sources)
   - `character.metadata.tsv`
   - `movie.metadata.tsv`
   - `plot_summaries.txt`
2. Run Data Preprocessing notebooks/scripts
- `prepare_movie_data.ipynb`
- `chunk_movie_data.ipynb`
- `build_movie_chunks_vectodb.ipynb`
- `get_movie_names_embeddings.py`
- `build_movie_names_vector_db.py`
3. Ensure Chroma collections are created and saved in Google Drive
4. Run Streamlit app
- Ensure the following are in Google Drive or uploaded into the Colab Notebook:
   - `movie_rag_pipeline.py`
   - `movie_rag_app.py`
- Get Ngrok **Authtoken**
   - Ngrok is free and a profile can be easily created using your Github Account
   - https://ngrok.com/docs/start
- Run:
   - `run_movie_rag_streamlit_app.ipynb`

---

## ✨ Features
- Interactive Chatbot 🤖
![Movie RAG Query Demo 2](assets/query2.gif)
- Side Search Bar
   - Finds movies in database
![Movie RAG Query Demo 3](assets/query3.gif)

---

## 🧠 How It Works

The system follows a standard RAG pipeline:

1. **Data Preparation**
   - Movie plots, metadata, and character data are cleaned and merged  

2. **Chunking**
   - Plot summaries are split using a sentence-based chunking strategy  

3. **Embedding**
   - Text chunks are converted into emeddings using: 
      - Sentence Transformers **all-mpnet-base-v2** model

4. **Vector Storage**
   - Embeddings are stored in a **ChromaDB** vector database  

5. **Retrieval**
   - Relevant chunks are retrieved based on user query similarity  

6. **Generation**
   - **Mistral-7B-Instruct** model generates responses using retrieved context  

7. **App Deployment**
    - Streamlit app run in Google Colab to leverage GPU resources for inference
    - Ngrok is used to create a secure public tunnel to the locally running Streamlit server

---

## 📁 Project Structure
```
movie-rag-system/
├── app_demo/
│   ├── build_movie_names_vectordb.py
│   ├── get_movie_names_embeddings.py
│   ├── movie_rag_app.py
│   ├── movie_rag_pipeline.py
│   ├── run_movie_rag_streamlit_app.ipynb
├── assets/
│   ├── query1.gif
│   ├── query2.gif
│   ├── query3.gif
├── data/
│   ├── movie_rag_eval_dataset.json
│   ├── movie_rag_evaluation.csv
├── evaluation/
│   ├── evaluate_mistral_responses.ipynb
│   ├── evaluation_explanations.md
│   ├── evaluation_summary.md
│   ├── run_movie_rag_eval.py
│   ├── testing.md
├── notebooks/
│   ├── build_movie_chunks_vectordb.ipynb
│   ├── chunk_movie_data.ipynb
│   ├── movie_rag_testing.ipynb
│   ├── plot_cleaning_breakdown.md
│   ├── prepare_movie_data.ipynb
├── .gitignore
├── README.md
```

---

## 📊 Data Sources

The dataset used in this project is derived from the CMU Movie Summary Corpus:

- CMU Movie Summary Corpus: https://www.cs.cmu.edu/~ark/personas/

This datasets used in this project includes:
- Movie metadata (genres, release dates, etc.)
- Character metadata
- Movie plot summaries

This data was collected by David Bamman, Brendan O'Connor, and Noah Smith at the Language Technologies Institute and Machine Learning Department at Carnegie Mellon University.