import json
import numpy as np
import nltk
from nltk.translate.bleu_score import corpus_bleu, sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
import sacrebleu
import pandas as pd


# Optional: pip install bert-score
try:
    from bert_score import score as bertscore_score
    HAS_BERTSCORE = True
except Exception:
    HAS_BERTSCORE = False

DATA_PATH = "movie_rag_eval_dataset.json"

nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
    
# Prepare data
def clean_text(text):
    return text.replace("\n", " ").strip()

smooth = SmoothingFunction().method1

# -------------------------
# BLEU prep
# -------------------------
bleu_references = [
    [nltk.word_tokenize(ref) for ref in item["references"]]
    for item in data
]
bleu_hypotheses = [
    nltk.word_tokenize(item["generated"])
    for item in data
]

sentence_bleu_scores = [
    sentence_bleu(refs, hyp, smoothing_function=smooth)
    for refs, hyp in zip(bleu_references, bleu_hypotheses)
]
corpus_bleu_score = corpus_bleu(
    bleu_references, bleu_hypotheses, smoothing_function=smooth
)

# -------------------------
# ROUGE
# -------------------------
rouge = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)

rouge1_scores, rouge2_scores, rougeL_scores = [], [], []
for item in data:
    # choose the best reference per metric by max F1
    ref_scores = [rouge.score(ref, item["generated"]) for ref in item["references"]]
    rouge1_scores.append(max(s["rouge1"].fmeasure for s in ref_scores))
    rouge2_scores.append(max(s["rouge2"].fmeasure for s in ref_scores))
    rougeL_scores.append(max(s["rougeL"].fmeasure for s in ref_scores))

# -------------------------
# METEOR
# -------------------------
meteor_scores = []
for item in data:
    ref_tokens = [nltk.word_tokenize(r) for r in item["references"]]
    gen_tokens = nltk.word_tokenize(item["generated"])
    meteor_scores.append(meteor_score(ref_tokens, gen_tokens))

# -------------------------
# TER / ChrF
# -------------------------
ter_scores = []
chrf_scores = []
for item in data:
    refs = item["references"]
    gen = item["generated"]
    ter_scores.append(min(sacrebleu.sentence_ter(gen, [ref]).score for ref in refs))
    chrf_scores.append(max(sacrebleu.sentence_chrf(gen, [ref]).score for ref in refs))

# -------------------------
# BERTScore
# -------------------------
if HAS_BERTSCORE:
    best_bert_f1 = []
    for item in data:
        cands = [item["generated"]] * len(item["references"])
        P, R, F1 = bertscore_score(cands, item["references"], lang="en", verbose=False)
        best_bert_f1.append(float(F1.max().item()))
else:
    best_bert_f1 = None

# -------------------------
# Summary
# -------------------------
print("=== Corpus / Macro Results ===")
print(f"Corpus BLEU: {corpus_bleu_score:.4f}")
print(f"Avg Sentence BLEU: {np.mean(sentence_bleu_scores):.4f}")
print(f"Avg ROUGE-1 F1: {np.mean(rouge1_scores):.4f}")
print(f"Avg ROUGE-2 F1: {np.mean(rouge2_scores):.4f}")
print(f"Avg ROUGE-L F1: {np.mean(rougeL_scores):.4f}")
print(f"Avg METEOR: {np.mean(meteor_scores):.4f}")
print(f"Avg TER (lower is better): {np.mean(ter_scores):.4f}")
print(f"Avg ChrF: {np.mean(chrf_scores):.4f}")
if best_bert_f1 is not None:
    print(f"Avg BERTScore F1: {np.mean(best_bert_f1):.4f}")
else:
    print("Avg BERTScore F1: skipped (install bert-score)")

rows = []
for i, item in enumerate(data, start=1):
    row = {
        "idx": i,
        "query": item["query"],
        "bleu": round(sentence_bleu_scores[i-1], 4),
        "rougeL": round(rougeL_scores[i-1], 4),
        "meteor": round(meteor_scores[i-1], 4),
        "ter": round(ter_scores[i-1], 4),
        "chrf": round(chrf_scores[i-1], 4),
    }
    if best_bert_f1 is not None:
        row["bertscore_f1"] = round(best_bert_f1[i-1], 4)
    rows.append(row)
# Convert to DataFrame
df = pd.DataFrame(rows)

# Save to CSV
df.to_csv("movie_rag_eval_results.csv", index=False)

print("CSV saved!")
