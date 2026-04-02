from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from src import config

class DocumentRetriever:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )

        self.qdrant_url = f"http://{config.HOST}:{config.PORT}"
        self.client = QdrantClient(self.qdrant_url, prefer_grpc=False)
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=config.NAME,
            embedding=self.embeddings
        )

    def get_relevant_documents(self, query: str, k: int = 3):
        print(f"Search in database on query: {query}")
        results = self.vector_store.similarity_search(query, k=k)
        print(f"Found {len(results)} results")
        return results


# Usage
if __name__ == "__main__":
    retriever = DocumentRetriever()
    user_question = "What is decorator?"

    docs = retriever.get_relevant_documents(user_question)
    for i, doc in enumerate(docs):
        print(f"\n--- Object №{i + 1} ---")
        print(f"Source: {doc.metadata.get('source')}")
        print(f"Text: {doc.page_content[:200]}")