import chromadb
from chromadb.config import Settings
import os
import logging

logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self, persist_directory="chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
    def get_or_create_collection(self, name):
        """
        Get or create a collection by name.
        """
        return self.client.get_or_create_collection(name=name)

    def add_documents(self, collection_name, documents, metadatas, ids):
        """
        Add documents to a collection.
        """
        collection = self.get_or_create_collection(collection_name)
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Added {len(documents)} documents to collection {collection_name}")

    def query(self, collection_name, query_text, n_results=5):
        """
        Query a collection for relevant documents.
        """
        collection = self.get_or_create_collection(collection_name)
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
