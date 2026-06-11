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


def build_where_filter(filters):
    if len(filters) == 0:
        return None

    if len(filters) == 1:
        key, value = filters[0]
        return {key: value}

    return {
        "$and": [
            {key: value} for key, value in filters
        ]
    }


@tool
def review_retriever(query: str) -> str:
    """
    Search restaurant reviews from ChromaDB with metadata filtering.
    """

    q = query.lower()
    filters = []

    if "hyderabad" in q:
        filters.append(("city", "Hyderabad"))
    elif "bangalore" in q:
        filters.append(("city", "Bangalore"))
    elif "chennai" in q:
        filters.append(("city", "Chennai"))

    if "biryani" in q:
        filters.append(("food_type", "Biryani"))
    elif "cafe" in q or "cafes" in q:
        filters.append(("food_type", "Cafe"))
    elif "italian" in q:
        filters.append(("food_type", "Italian"))

    if "compare paradise and bawarchi" in q or "paradise and bawarchi" in q:
        results = collection.query(
            query_texts=[query],
            n_results=10,
            where={"food_type": "Biryani"}
        )

        docs = results["documents"][0]

        filtered_docs = [
            doc for doc in docs
            if "Restaurant Name: Paradise" in doc
            or "Restaurant Name: Bawarchi" in doc
        ]

        if not filtered_docs:
            return "No matching reviews found for Paradise and Bawarchi."

        return "\n\n\n".join(filtered_docs)

    if "paradise" in q:
        filters.append(("restaurant_name", "Paradise"))
    elif "bawarchi" in q:
        filters.append(("restaurant_name", "Bawarchi"))

    n = 5

    if "best" in q or "serves the best" in q:
        n = 10

    where_filter = build_where_filter(filters)

    if where_filter:
        results = collection.query(
            query_texts=[query],
            n_results=n,
            where=where_filter
        )
    else:
        results = collection.query(
            query_texts=[query],
            n_results=n
        )

    docs = results["documents"][0]

    if not docs:
        return "No matching reviews found."

    return "\n\n\n".join(docs)