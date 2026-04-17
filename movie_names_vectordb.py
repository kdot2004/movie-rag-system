"""
Create the `movie_titles` Chroma collection used by the title-search feature
in `movie_rag_app.py`.

This script loads:
- `movie_titles.txt`              -> list of movie titles
- `movie_title_embeddings.npy`    -> precomputed embeddings for those titles

It then creates and populates a new Chroma collection named `movie_titles`.

NOTE:
Both `movie_titles.txt` and `movie_title_embeddings.npy` are required to run
this script and the `movie_rag_app.py`.

- `movie_titles.txt` is available on GitHub.
- `movie_title_embeddings.npy` is not included in the repository due to its size.
  Please request this file separately before running the script.

Before running:
1. Install all required project dependencies.
2. Place this script, `movie_titles.txt`, and `movie_title_embeddings.npy`
   in the same working directory.
3. Set the `chromadb.PersistentClient()` path to the same directory as your
   existing Chroma database.

After running successfully, the `movie_titles` collection will be created and
can be loaded by the app to support movie title search.

Expected collection size: 39,915 entries.
"""


# Import chromadb
import chromadb

# Store movie titles in a list
with open("movie_titles.txt", "r", encoding="utf-8") as f:
    movies = [line.strip() for line in f]

# Load embeddings 
import numpy as np
embeddings = np.load("movie_title_embeddings.npy")

#  Populate IDs list (list of indices for movies)
ids = [str(i) for i in range(len(movies))]

# Set up client
client = chromadb.PersistentClient("") # Whatever file path your current chromadb file is 

# Create new collection
movie_titles = client.get_or_create_collection("movie_titles")

# Find the max batch size for batch processing
max_batch_size = client.get_max_batch_size() - 100

# Move data to collection in batches
for i in range(0, len(movies), max_batch_size):
    movie_titles.add(
        ids=ids[i:i + max_batch_size],
        documents=movies[i:i + max_batch_size],
        embeddings=embeddings[i:i + max_batch_size]
    )
    print(f"Added {min(i + max_batch_size, len(ids))}/{len(ids)}")

# Print total num of entries in collection
print(movie_titles.count()) # Should be 39,915