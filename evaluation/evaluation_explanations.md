# Movie RAG System Evaluation

## Overview
This project evaluates a **Movie Retrieval-Augmented Generation (RAG)** system. The evaluation consists of two key components:
- **Retrieval**: Assessing the effectiveness of retrieving relevant documents.
- **Text Generation**: Evaluating the fluency and quality of the generated responses.

## Evaluation Process

### 1. **Retrieval Evaluation**
The **retrieval** component of the system is evaluated using **Precision**. Precision measures how many of the top-k retrieved documents are relevant to the query. We use `top_k = 5` for all queries, and a precision score is calculated based on the relevance of the retrieved documents.

#### Example Evaluation for Retrieval:
For the query **"What is the plot of The Hunger Games?"**:
- The system retrieves 5 documents, 4 of which are relevant.
- **Precision@5**: 0.8

### 2. **Text Generation Evaluation**
The **text generation** aspect is assessed using a variety of metrics that evaluate the fluency and quality of the model-generated responses.

#### Key Metrics for Text Generation:
1. **BLEU (BiLingual Evaluation Understudy)**:
   - Measures exact overlap based on n-gram precision.
   - **Corpus BLEU**: Evaluates the overall match for a set of queries.
   - **Sentence BLEU**: Sentence-level performance.

2. **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**:
   - Measures recall of n-grams between generated responses and references.
   - We use **ROUGE-1**, **ROUGE-2**, and **ROUGE-L** for comprehensive quality evaluation.

3. **METEOR**:
   - Accounts for synonyms, stemming, and paraphrases, offering a more nuanced comparison than BLEU.

4. **TER (Translation Edit Rate)**:
   - Measures the number of edits required to match the generated text with the reference text.

5. **ChrF**:
   - Character-level precision and recall, useful for detecting fine-grained text differences.

6. **BERTScore**:
   - Utilizes pre-trained BERT models to assess semantic similarity between the generated and reference texts.

7. **Latency**:
   - Measures the time taken to generate a response after the context is provided, essential for performance benchmarking.

#### Most Important Metrics for RAG Systems:
The following metrics were prioritized for the RAG system (in order of importance):

1. **BERTScore**: Measures semantic similarity using pre-trained BERT models, ideal for RAG where meaning and paraphrasing are crucial.
2. **ROUGE**: Focuses on recall, ensuring the system captures all relevant information from references.
3. **METEOR**: Accounts for synonyms and paraphrases, better than BLEU for handling variations while maintaining meaning.
4. **BLEU**: Measures exact n-gram overlap but is weak for RAG systems due to its inability to handle paraphrasing effectively.
5. **ChrF**: Useful for fine-grained text differences such as morphology and spelling variations.
6. **TER**: Least important for RAG, as it focuses on exact matches rather than meaning.

## Dataset and Files

The dataset used for the evaluation contains the test queries, reference responses, and model-generated outputs. The dataset was created manually and with AI-generated content, ensuring a mix of both.

### Data Files:
- **`movie_rag_eval_dataset.json`**: Contains the queries, reference responses, and model outputs in JSON format. This file is used for both retrieval and text generation evaluations.
- **`movie_rag_eval_dataset.csv`**: A CSV file of the evalaution results for each test query.

### File Descriptions:
- **`movie_rag_eval_dataset.json`**:  
  - Format: JSON  
  - Contains three fields: `query`, `reference`, and `model_response`.
  - Provides a structured format for evaluating both retrieval and text generation.

- **`movie_rag_evaluation.csv`**:  
  - Format: CSV  
  - Includes columns for `query`, `bleu`, `rouge:`, `precision`, `bleu`, etc.
  - A tabular version of the evaluation results data.