'''
import chromadb
from chromadb.utils import embedding_functions

class RegulatoryMemory:
    def __init__(self, storage_path="./chroma_db"):
        # 1. Initialize Persistent Client (saves data to disk)
        self.client = chromadb.PersistentClient(path=storage_path)
        
        # 2. Use a standard open-source embedding function
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        
        # 3. Get or create a collection for regulatory history
        self.collection = self.client.get_or_create_collection(
            name="reg_history", 
            embedding_function=self.ef
        )

    def add_memory(self, doc_id, text, metadata):
        """Adds a new regulatory interpretation to the database."""
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        print(f"Memory Saved: {doc_id}")

    def query_past_cases(self, query_text, n_results=2):
        """Retrieves similar past regulatory changes."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

# Example Usage
if __name__ == "__main__":
    mem = RegulatoryMemory()
    
    # Storing a past event
    mem.add_memory(
        doc_id="REG-2024-001",
        text="Standardized approach for credit risk requires 8% capital floor.",
        metadata={"regulator": "Basel", "year": 2024}
    )
    
    # Searching for context
    past_info = mem.query_past_cases("What is the capital requirement for credit risk?")
    print("Found in Memory:", past_info['documents'])
'''
