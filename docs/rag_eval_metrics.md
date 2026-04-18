## 📊 RAG Evaluation Cheat Sheet (Precision@k, Recall@k, Latency)

### 🎯 Purpose

This guide defines how we evaluate retrieval performance in our RAG system.
Use this consistently across all queries to ensure fair and accurate comparisons.

---

## ✅ 1. Precision@k

**Definition:**
The proportion of retrieved documents that are relevant.

**Formula:**
Precision@k = (Number of relevant documents in top k) / k

**Example (k = 5):**

* Retrieved documents: 5
* Relevant documents among them: 4

→ Precision@5 = 4 / 5 = **0.8**

**Interpretation:**

* High precision → fewer irrelevant results
* Low precision → noisy retrieval

---

## ✅ 2. Recall@k

**Definition:**
The proportion of all relevant documents that were successfully retrieved.

**Formula:**
Recall@k = (Number of relevant documents in top k) / (Total number of relevant documents in dataset)

---

### ⚠️ Important: What counts as “relevant”?

Relevant ≠ all documents about the same movie

Relevant = documents that actually help answer the query

---

### Example:

**Query:** “What is the plot of The Hunger Games?”

In the dataset:

* Total Hunger Games documents: 8
* Documents that actually contain plot info: 5 → ✅ THESE are relevant

If retrieval returns:

* 4 relevant plot documents

→ Recall@5 = 4 / 5 = **0.8**

---

## 🚨 Common Mistake (Avoid This)

❌ Using all documents about a movie as “relevant”
✔️ Only count documents that directly answer the query

---

## ✅ 3. Latency

**Definition:**
Time taken to retrieve and generate a response.

**Measured as:**

* End-to-end response time (seconds)

**Example:**

* Query → Response time = 1.25s

→ Latency = **1.25s**

---

## 🧠 Summary Table

| Metric      | Measures                         | Goal             |
| ----------- | -------------------------------- | ---------------- |
| Precision@k | How many retrieved are relevant  | Reduce noise     |
| Recall@k    | How many relevant were retrieved | Improve coverage |
| Latency     | Speed of system                  | Faster responses |

---

## 💡 Best Practices

* Always define **relevant documents per query**
* Keep k consistent (we use k = 5)
* Use both:

  * **Qualitative evaluation** (markdown examples)
  * **Quantitative metrics** (this section)

---

## 🚀 How We Use This

For each query:

1. Identify ground-truth relevant documents
2. Count how many were retrieved in top k
3. Compute:

   * Precision@k
   * Recall@k
   * Latency

---

## 🔁 Quick Template (Copy Per Query)

```
Precision@5: 
Recall@5: 
Latency: 

Relevant Docs (Ground Truth):
- 

Retrieved Relevant Docs:
- 
```
