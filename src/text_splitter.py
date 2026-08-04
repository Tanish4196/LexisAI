"""
Text Splitter Module

Splits extracted documents into overlapping chunks
while preserving metadata for RAG retrieval.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


class TextSplitter:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=CHUNK_SIZE,

            chunk_overlap=CHUNK_OVERLAP,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split_document(self, pages, filename):

        """
        Parameters
        ----------
        pages : list

            Example:

            [
                {
                    "page":1,
                    "text":"....."
                }
            ]

        filename : str

        Returns
        -------

        List of chunk dictionaries
        """

        chunks = []

        chunk_id = 0

        for page in pages:

            page_number = page["page"]

            text = page["text"]

            split_text = self.splitter.split_text(text)

            for chunk in split_text:

                chunks.append(

                    {

                        "chunk_id": chunk_id,

                        "source": filename,

                        "page": page_number,

                        "text": chunk

                    }

                )

                chunk_id += 1

        return chunks