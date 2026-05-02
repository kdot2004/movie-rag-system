"""
This script prepares the embeddings and
movie titles for: build_movie_names_vectordb.py


NOTE:
- Ensure the csv file: merged_movie_rag is in the correct directory
- Make sure to alter path when saving numpy embeddings
"""
# Load csv file
import pandas as pd
df = pd.read_csv("merged_movie_rag.csv")

# Extract unique movie names
movie_names = df['movie_name'].drop_duplicates().to_list()

# Store in a text file
with open("movie_titles.txt", "w", encoding="utf-8") as f:
    for name in movie_names:
        f.write(name + "\n")

# Load sentence transformers model
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-mpnet-base-v2")

# Compute embeddings
embeddings = model.encode(movie_names, show_progress_bar=True)

# Save embeddings
import numpy as np
np.save("desired_path.npy", embeddings)