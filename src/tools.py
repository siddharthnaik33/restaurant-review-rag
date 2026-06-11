import chromadb
from chromadb.utils import embedding_functions
from langchain.tools import tool

client = chromadb.PersistentClient(path="chroma_db")

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_collection(
    name="restaurant_reviews",
    embedding_function=embedding_fn
)

@tool
def review_retriever(query: str) -> str:
    """
    Search restaurant reviews from ChromaDB.
    """

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    docs = results["documents"][0]

    if not docs:
        return "No reviews found."

    return "\n\n".join(docs)