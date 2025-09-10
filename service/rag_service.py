from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class RAGService:
    def __init__(self):
        self.document_paths = ["RAG_CONTEXT/java_code_standards.txt", "RAG_CONTEXT/python_code_standards.txt"]
        self.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.vectorstore = None
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        try:
            all_documents = []
            for doc_path in self.document_paths:
                loader = TextLoader(doc_path)
                all_documents.extend(loader.load())
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_documents(all_documents)

            embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
            self.vectorstore = FAISS.from_documents(texts, embeddings)
        except Exception as e:
            print(f"Error initializing vectorstore: {e}")
            self.vectorstore = None

    def retrieve_context(self, query: str, k: int = 4) -> str:
        if not self.vectorstore:
            print("Vectorstore not initialized. Cannot retrieve context.")
            return ""
        
        docs = self.vectorstore.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context
