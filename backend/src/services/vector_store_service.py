import hashlib

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from utils.text import normalize_whitespace


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

    @staticmethod
    async def _get_document_id_prefix(metadata: dict) -> str:
        resume_id = metadata["resume_id"]
        doc_type = metadata.get("type", "default")
        entity = metadata.get("entity")

        entity_suffix = f"_{hashlib.md5(entity.encode()).hexdigest()}" if entity else ""

        return f"{resume_id}_{doc_type}{entity_suffix}"

    async def _split_text(self, text: str, metadata: dict) -> list[Document]:
        chunks = self.splitter.split_text(normalize_whitespace(text))
        return [
            Document(page_content=chunk.strip(" \n\t●-–"), metadata=metadata)
            for chunk in chunks
        ]

    async def add_document(self, text: str, metadata: dict):
        documents = await self._split_text(text, metadata)
        prefix = await self._get_document_id_prefix(metadata)
        ids = [f"{prefix}_chunk_{i}" for i in range(len(documents))]

        await self.store.aadd_documents(documents, ids=ids)

    async def retrieve(self, query: str, resume_id: str, k: int = 5):
        results = await self.store.asimilarity_search(
            query, k=k, filter={"resume_id": resume_id}
        )
        return [doc.page_content for doc in results]

    async def get_documents(self, resume_id: str):
        return await self.store.asimilarity_search(
            query="", k=100, filter={"resume_id": resume_id}
        )

    async def refresh_document(self, text: str, metadata: dict):
        resume_id = metadata["resume_id"]
        doc_type = metadata.get("type", "default")

        if resume_id and doc_type:
            prefix = await self._get_document_id_prefix(metadata)
            ids = [f"{prefix}_chunk_{i}" for i in range(10)]

            self.store.delete(ids=ids)

        await self.add_document(text, metadata)
