"""
Embeddings Module

Uses HuggingFace Sentence Transformers
to generate embeddings for documents
and user queries.
"""

import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL


@st.cache_resource
def load_embedding_model():
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    return SentenceTransformer(EMBEDDING_MODEL)


class EmbeddingModel:
    """
    Loads the embedding model only once.
    """

    _model = None

    def __init__(self):

        if EmbeddingModel._model is None:
            EmbeddingModel._model = load_embedding_model()

        self.model = EmbeddingModel._model

    # -----------------------------------
    # Document Embeddings
    # -----------------------------------

    def create_document_embeddings(self, chunks):

        """
        Parameters
        ----------
        chunks : List[dict]

        Example:

        [
            {
                "text":"....",
                "page":1
            }
        ]

        Returns
        -------

        numpy.ndarray
        """

        texts = [

            chunk["text"]

            for chunk in chunks

        ]

        embeddings = self.model.encode(

            texts,

            convert_to_numpy=True,

            show_progress_bar=True

        )

        return embeddings.astype(np.float32)

    # -----------------------------------
    # Query Embedding
    # -----------------------------------

    def create_query_embedding(self, query):

        embedding = self.model.encode(

            [query],

            convert_to_numpy=True

        )

        return embedding.astype(np.float32)

    # -----------------------------------
    # Embedding Dimension
    # -----------------------------------

    def get_dimension(self):

        return self.model.get_sentence_embedding_dimension()