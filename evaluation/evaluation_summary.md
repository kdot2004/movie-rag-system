# Evaluation Summary

| Metric                | Value     | 
|-----------------------|-----------|
| **Average Precision**  | 0.55      |
| **Average Latency**    | 13.73     | 
| **BERTScore**          | 0.8861    |
| **ROUGE-1 F1**         | 0.3325    | 
| **ROUGE-2 F1**         | 0.1607    | 
| **ROUGE-L F1**         | 0.2714    | 
| **METEOR**             | 0.4255    | 
| **BLEU**               | 0.0729    | 
| **ChrF**               | 39.6788   | 
| **TER**                | 302.4843  | 

# Key Takeaways:
1. Strong Semantic Alignment: BERTScore is the standout metric, showing that the system effectively captures the meaning behind the queries.
2. The system does a fair job at identifying relevant documents, but improvements in ranking could increase the proportion of relevant documents retrieved.
    - Switching to more sophisticated chunking strategies like LangChain's Text Splitter could help improve precision by preserving context and increasing the relevance of the retrieved documents.
    - A more specialized embedding model, (perhaps one good for long documents such as movie plots), could enhance the system’s ability to capture semantic relationships and improve retrieval accuracy.
3. An average latency of 13.73 seconds is a bit high, but given the variety of queries tested, including more complex multi-step queries, this delay is somewhat expected. Despite this, latency should be improved to ensure a smoother user experience, especially for real-time applications.
