from .vector_db import VectorDB

class Retriever:
    def __init__(self, vector_db_path="chroma_db"):
        self.db = VectorDB(persist_directory=vector_db_path)

    def get_context(self, domain, query, n_results=3):
        """
        Retrieve context for a specific domain.
        """
        results = self.db.query(domain, query, n_results=n_results)
        
        # Flatten results
        if results and results['documents']:
            return "\n\n".join(results['documents'][0])
        return ""
