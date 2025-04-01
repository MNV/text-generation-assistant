from typing import List, Dict
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

from services.entity_research_service import EntityResearchService
from services.user_entity_service import UserEntityService

load_dotenv()


class RAGService:
    def __init__(
        self,
        user_entity_service: UserEntityService,
        entity_research_service: EntityResearchService,
    ):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.embedding_model = OpenAIEmbeddings(
            model="text-embedding-ada-002", openai_api_key=self.api_key
        )
        self.vectorstore = Chroma(
            embedding_function=self.embedding_model, persist_directory="./data/chroma"
        )
        self.llm = ChatOpenAI(model="gpt-4o", openai_api_key=self.api_key)

    def store_document(self, document: str, metadata: dict):
        """Store documents in ChromaDB with metadata."""
        self.vectorstore.add_texts(texts=[document], metadatas=[metadata])
        self.vectorstore.persist()

    async def fetch_researched_content(self, user_id: str) -> Dict[str, str]:
        """Fetch researched content for user-selected entities."""
        selections = await self.user_entity_service.get_user_selections(user_id)
        entity_texts = [selection["entity"] for selection in selections]
        return await self.entity_research_service.research_entities(
            entity_texts, user_id
        )

    def retrieve_context(self, query: str, user_id: str, role: str = None) -> List[str]:
        """Retrieve relevant documents based on a query and role."""
        filters = {"user_id": user_id}
        if role:
            filters["role"] = role
        results = self.vectorstore.similarity_search(query, k=5, filters=filters)
        return [result.page_content for result in results]

    async def generate_recommendation(
        self,
        query: str,
        principal_id: str,
        grantee_id: str,
        directives: str,
        circumstances: str,
    ) -> str:
        """Generate recommendation letter using RAG with enriched context."""
        principal_context = await self.fetch_researched_content(principal_id)
        grantee_context = await self.fetch_researched_content(grantee_id)

        # Prepare enriched context for RAG
        enriched_context = "\n".join(
            [
                f"Principal's Expertise:\n"
                + "\n".join([f"{k}: {v}" for k, v in principal_context.items()]),
                f"Grantee's Skills and Achievements:\n"
                + "\n".join([f"{k}: {v}" for k, v in grantee_context.items()]),
            ]
        )

        custom_prompt = (
            f"Generate a recommendation letter considering the following:\n"
            f"- Principal's expertise and authority.\n"
            f"- Grantee's skills and achievements.\n"
            f"- Circumstances: {circumstances}\n"
            f"- Directives: {directives}\n"
            f"- Context:\n{enriched_context}\n"
            f"Query: {query}"
        )

        retriever = self.vectorstore.as_retriever()
        rag_chain = RetrievalQA(llm=self.llm, retriever=retriever)
        result = rag_chain.run(custom_prompt)

        return result
