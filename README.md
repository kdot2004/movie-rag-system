# 🎬 Movie RAG System
> 🚀 A Retrieval-Augmented Generation system for intelligent movie search and discovery.

---

## 📌 Overview
This project implements a Retrieval-Augmented Generation (RAG) system designed to answer movie-related questions. 

The system combines information retrieval from an external dataset with LLM-based response generation, ensuring that outputs are grounded in real data. The goal was to build a system capable of answering various queries types, including plot-based questions, actor and character inquiries, metadata lookups, and recommendation-style prompts.

---

## 📸 Demo
[Youtube Link](https://youtu.be/107usbwWhow?si=lm6dqRxsn1LxVp0t)

---

## 🧠 How It Works

The system follows a standard RAG pipeline:

1. **Data Preparation**
   - Movie plots, metadata, and character data are cleaned and merged  

2. **Chunking**
   - Plot summaries are split using a sentence-based chunking strategy  

3. **Embedding**
   - Text chunks are converted into vector representations using a sentence transformer model: **all-mpnet-base-v2**

4. **Vector Storage**
   - Embeddings are stored in a ChromaDB vector database  

5. **Retrieval**
   - Relevant chunks are retrieved based on user query similarity  

6. **Generation**
   - Mistral-7B-Instruct model generates responses using retrieved context  

7. **App Deployment**
    - The application is developed using Streamlit and executed in a Google Colab environment to leverage GPU resources.
    - Ngrok is used to create a secure public tunnel to the locally running Streamlit server.

---

## 📁 Project Structure
```
movie-rag-system/
├── app/
│   └── movie_rag_app.py
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
├── notebooks/
│   └── data_cleaning.ipynb
├── src/
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retrieval.py
│   └── generation.py
├── evaluation/
│   ├── test_queries.json
│   └── evaluate.py
├── requirements.txt
└── README.md

## 📊 Data Sources

The dataset used in this project is derived from the CMU Movie Summary Corpus:

- CMU Movie Summary Corpus: https://www.cs.cmu.edu/~ark/personas/

This datasets used in this project includes:
- Movie metadata (genres, release dates, etc.)
- Character metadata
- Movie plot summaries

This data was collected by David Bamman, Brendan O'Connor, and Noah Smith at the Language Technologies Institute and Machine Learning Department at Carnegie Mellon University.