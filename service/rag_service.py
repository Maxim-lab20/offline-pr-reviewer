from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Weaviate
from weaviate.client import WeaviateClient
from weaviate import connect_to_local


class RAGService:
    def __init__(self):
        self.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.vectorstore = None
        self.weaviate_client = connect_to_local()
        self.collection_name = "CodeStandards"
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        try:
            if self.weaviate_client.collections.exists(self.collection_name):
                self.vectorstore = Weaviate(client=self.weaviate_client, collection_name=self.collection_name, embedding=HuggingFaceEmbeddings(model_name=self.embedding_model_name))
                return
            
            # If the collection does not exist, create an empty one
            self.weaviate_client.collections.create(self.collection_name)
            self.vectorstore = Weaviate(client=self.weaviate_client, collection_name=self.collection_name, embedding=HuggingFaceEmbeddings(model_name=self.embedding_model_name))
        except Exception as e:
            print(f"Error initializing vectorstore: {e}")
            self.vectorstore = None

    def ingest_documents(self, documents):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_documents(documents)
            embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
            if self.vectorstore:
                self.vectorstore.add_documents(texts)
            else:
                self.vectorstore = Weaviate.from_documents(texts, embeddings, client=self.weaviate_client, collection_name=self.collection_name)
            print(f"Successfully ingested {len(documents)} documents.")
        except Exception as e:
            print(f"Error ingesting documents: {e}")

    def retrieve_context(self, query: str, k: int = 4) -> str:
        if not self.vectorstore:
            print("Vectorstore not initialized. Cannot retrieve context.")
            return ""
        
        docs = self.vectorstore.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context
