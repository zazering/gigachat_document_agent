import os
import glob
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from src import config
from src.config import CHUNK_OVERLAP


class DocumentIngestor:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        self.embeddings = None

    def get_loader(self, file_path: str):
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == ".txt":
            return TextLoader(file_path, encoding="utf-8")
        elif ext == ".pdf":
            return PyPDFLoader(file_path)
        elif ext == ".docx":
            return Docx2txtLoader(file_path)
        else:
            print(f"Unsupported file type: {ext}")
            return None

    def load_documents(self) -> List[Document]:
        print(f"Scanning directory: {self.data_dir}")
        all_documents = []
        search_pattern = os.path.join(self.data_dir, "*")
        file_paths = glob.glob(search_pattern)

        if not file_paths:
            print(f"Directory {search_pattern} does not contain any files or doesn't exist")
            return []

        for file_path in file_paths:
            if not os.path.isfile(file_path):
                continue
            loadder = self.get_loader(file_path)
            if loadder:
                print(f"Loading {file_path}")
                try:
                    docs = loadder.load()
                    all_documents.extend(docs)
                except Exception as e:
                    print(f"Failed to load {file_path}: {e}")
        print(F"Found {len(all_documents)} documents")
        return all_documents

    def split_text(self, document: List[Document]) -> List[Document]:
        print(f"Splitting {len(document)} document")
        chunks = self.text_splitter.split_documents(document)
        print(f"Found {len(chunks)} chunks")
        return chunks

    def save_to_database(self, chunks: List[Document]):
        if not chunks:
            print("Nothing to save")
            return
        print(f"Initializing database with {len(chunks)} chunks: {config.EMBEDDING_MODEL}")
        self.embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL, model_kwargs={'device': 'cpu'})

        qdrant_url= f"http://{config.HOST}:{config.PORT}"
        print(f"Loading embeddings in qdrant collection: {config.NAME}")
        Qdrant.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            url=qdrant_url,
            collection_name=config.NAME,
            prefer_grpc=False,
        )
        print("Database saved")

    def run(self):
        raw_docs = self.load_documents()
        if not raw_docs:
            print("No documents to ingestor")
            return
        chunks = self.split_text(raw_docs)
        self.save_to_database(chunks)
        print("Preparing done")

# Usage
if __name__ == "__main__":
    ingestor = DocumentIngestor()
    ingestor.run()