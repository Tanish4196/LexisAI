"""
FAISS Vector Store

Stores document embeddings and performs
semantic similarity search.
"""

import os
import pickle
import faiss
import numpy as np

from src.config import (
    FAISS_INDEX_PATH,
    METADATA_PATH
)


class VectorStore:

    def __init__(self):
        self.index = None
        self.metadata = []

    # -------------------------------------
    # Create Index
    # -------------------------------------

    def create_index(self, embeddings, chunks):
        """
        Parameters
        ----------
        embeddings : numpy.ndarray
        chunks : list of dictionaries
        """
        if len(chunks) == 0 or embeddings is None or len(embeddings) == 0 or len(embeddings.shape) < 2:
            self.index = None
            self.metadata = []
            return

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        self.metadata = chunks

    # -------------------------------------
    # Save Index
    # -------------------------------------

    def save(self):
        if self.index is None:
            return

        faiss.write_index(
            self.index,
            str(FAISS_INDEX_PATH)
        )

        with open(METADATA_PATH, "wb") as f:
            pickle.dump(
                self.metadata,
                f
            )

    # -------------------------------------
    # Load Index
    # -------------------------------------

    def load(self):
        if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(METADATA_PATH):
            self.index = None
            self.metadata = []
            return False

        try:
            self.index = faiss.read_index(
                str(FAISS_INDEX_PATH)
            )
            with open(METADATA_PATH, "rb") as f:
                self.metadata = pickle.load(f)
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            self.index = None
            self.metadata = []
            return False

    # -------------------------------------
    # Search
    # -------------------------------------

    def search(self, query_embedding, k=3):
        """
        Returns top-k most similar chunks.
        """
        if self.index is None or len(self.metadata) == 0:
            return []

        search_k = min(k, self.index.ntotal)
        if search_k <= 0:
            return []

        distances, indices = self.index.search(
            query_embedding,
            search_k
        )

        results = []
        for distance, idx in zip(
            distances[0],
            indices[0]
        ):
            if idx == -1 or idx >= len(self.metadata):
                continue

            chunk = self.metadata[idx].copy()
            chunk["score"] = float(distance)
            results.append(chunk)

        return results

    # -------------------------------------
    # Total Chunks
    # -------------------------------------

    def total_chunks(self):
        return len(self.metadata)

    # -------------------------------------
    # Reset Index
    # -------------------------------------

    def clear(self):
        self.index = None
        self.metadata = []

        if os.path.exists(FAISS_INDEX_PATH):
            try:
                os.remove(FAISS_INDEX_PATH)
            except Exception:
                pass

        if os.path.exists(METADATA_PATH):
            try:
                os.remove(METADATA_PATH)
            except Exception:
                pass