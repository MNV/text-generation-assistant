from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


class VectorStoreService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.store = Chroma(
            embedding_function=self.embeddings, persist_directory="./data/chroma"
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=70,
            separators=["\n\n", "\n", ".", "!", "?", ";", ",", " "],
        )

    async def _split_text(self, text: str, metadata: dict) -> list[Document]:
        chunks = self.splitter.split_text(text)
        return [
            Document(page_content=chunk.strip(" \n\t●-–"), metadata=metadata)
            for chunk in chunks
        ]

    async def add_document(self, text: str, metadata: dict):
        documents = await self._split_text(text, metadata)

        ids = [f"{metadata['resume_id']}_chunk_{i}" for i in range(len(documents))]
        self.store.add_documents(documents, ids=ids)
        self.store.persist()

    async def retrieve(self, query: str, resume_id: str, k: int = 5):
        results = self.store.similarity_search(
            query, k=k, filter={"resume_id": resume_id}
        )
        return [doc.page_content for doc in results]

    async def get_documents(self, resume_id: str):
        return self.store.similarity_search(
            query="", k=100, filter={"resume_id": resume_id}
        )

    async def refresh_document(self, text: str, metadata: dict):
        if document_id := metadata.get("resume_id"):
            ids = [f"{document_id}_chunk_{i}" for i in range(100)]
            self.store.delete(ids=ids)

        await self.add_document(text, metadata)
