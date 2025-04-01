from langchain_chroma import Chroma
from schemas.ner import NERResult
from langchain_openai import OpenAIEmbeddings


class VectorStoreService:
    def __init__(self):
        self.store = Chroma(
            embedding_function=OpenAIEmbeddings(
                model="text-embedding-3-small", dimensions=512
            ),
            collection_name="entities",
        )

    async def store_entities(self, user_id: str, ner_result: NERResult):
        collection = self.store.get_or_create_collection("entities")
        for label, entities in ner_result.entities.items():
            for entity in entities:
                collection.add(
                    documents=[entity.text],
                    metadatas=[{"label": label, "language": entity.language}],
                    ids=[f"{user_id}:{entity.text}"],
                )

    async def search_entities(self, query: str):
        collection = self.store.get_collection("entities")
        results = collection.query(query_texts=[query], n_results=5)
        return results
