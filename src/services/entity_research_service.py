import os
import httpx
from typing import List, Dict
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()


class EntityResearchService:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.vectorstore = Chroma(
            embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),
            persist_directory="./data/chroma",
        )

    async def fetch_entity_info(self, entity: str) -> str:
        """Fetch information about an entity using Perplexity API."""
        url = "https://api.perplexity.ai/search"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"query": entity, "num_results": 3}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            summaries = [item["summary"] for item in data.get("results", [])]
            return "\n".join(summaries)

    async def research_entities(
        self, entities: List[str], user_id: str
    ) -> Dict[str, str]:
        """Research selected entities and store content in ChromaDB."""
        researched_content = {}
        for entity in entities:
            info = await self.fetch_entity_info(entity)
            researched_content[entity] = info
            self.vectorstore.add_texts(
                texts=[info], metadatas=[{"entity": entity, "user_id": user_id}]
            )
        self.vectorstore.persist()
        return researched_content
