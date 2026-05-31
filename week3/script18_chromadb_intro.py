import os

import chromadb


client = chromadb.Client()

collection = client.get_or_create_collection(
    name="bubble_tea_menu"
)

collection.add(
    documents=["Mango milk tea with tapioca pearls", "Mango smoothie with lychee jelly", "Quarterly financial report Q3"],
    metadatas=[{"source": "menu"}, {"source": "menu"}, {"source": "report"}],
    ids=["1", "2", "3"]
)

print(collection.query(
    query_texts=["I want a mango drink"],
    n_results=1
))