from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_weaviate import WeaviateVectorStore
from langchain.schema import Document
import weaviate


class RAGService:
    def __init__(self):
        self.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
        self.index_name = "Test"
        self.text_key = "text"

    def ingest_document(self, documents: list[Document]):
        """Ingests a list of LangChain Document objects"""
        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = splitter.split_documents(documents)

        # Add docs into Weaviate
        with weaviate.connect_to_local() as client:
            # Clear existing data to ensure new ingests override previous ones
            try:
                collection = client.collections.get(self.index_name)
                # Delete all objects that have the text field (effectively clears collection)
                collection.data.delete_many(
                    where={
                        "operator": "IsNotNull",
                        "path": [self.text_key]
                    }
                )
            except Exception:
                # If collection does not exist yet, proceed to creation on add
                pass
            vectorstore = WeaviateVectorStore(
                client=client,
                index_name=self.index_name,
                text_key=self.text_key,
                embedding=self.embeddings,
            )
            vectorstore.add_documents(split_docs)

    def list_documents(self, limit: int = 10):
        """Fetch ingested documents from Weaviate v4"""
        with weaviate.connect_to_local() as client:
            collection = client.collections.get(self.index_name)

            # Fetch documents
            results = collection.query.fetch_objects(limit=limit)

            # Convert to a simple list of dicts
            docs = []
            for o in results.objects:
                props = o.properties
                props["uuid"] = str(o.uuid)  # include ID for reference
                docs.append(props)

        return docs

    def retrieve_context(self, query: str, k: int = 4) -> str:
        """Retrieve top-k similar docs as context"""
        with weaviate.connect_to_local() as client:
            vectorstore = WeaviateVectorStore(
                client=client,
                index_name=self.index_name,
                text_key=self.text_key,
                embedding=self.embeddings,
            )
            docs = vectorstore.similarity_search(query, k=k)

        return "\n\n".join([doc.page_content for doc in docs])
