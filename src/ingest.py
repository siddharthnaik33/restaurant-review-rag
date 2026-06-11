import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

CSV_PATH = "data/restaurant_reviews.csv"
DB_PATH = "chroma_db"

REQUIRED_COLUMNS = [
    "restaurant_id",
    "restaurant_name",
    "city",
    "food_type",
    "rating",
    "review_text",
    "review_date",
    "customer_name",
]


def clean_data(df):
    df = df.dropna(subset=["restaurant_id", "restaurant_name", "city", "food_type", "rating", "review_text"])
    df = df.drop_duplicates(subset=["restaurant_id", "review_text"])

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")

    df = df.dropna(subset=["rating", "review_date"])

    return df


def ingest_reviews():
    df = pd.read_csv(CSV_PATH)

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    df = clean_data(df)

    client = chromadb.PersistentClient(path=DB_PATH)

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name="restaurant_reviews",
        embedding_function=embedding_fn
    )

    ids = []
    documents = []
    metadatas = []

    for index, row in df.iterrows():
        document = f"""
Restaurant Name: {row['restaurant_name']}
City: {row['city']}
Food Type: {row['food_type']}
Rating: {row['rating']}
Review Date: {row['review_date'].date()}
Customer Name: {row['customer_name']}
Review Text: {row['review_text']}
"""

        ids.append(f"{row['restaurant_id']}_{index}")
        documents.append(document)
        metadatas.append({
            "restaurant_name": str(row["restaurant_name"]),
            "city": str(row["city"]),
            "food_type": str(row["food_type"]),
            "rating": float(row["rating"]),
            "review_date": str(row["review_date"].date()),
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print("Data ingested successfully into ChromaDB.")
    print(f"Total reviews stored: {len(ids)}")


if __name__ == "__main__":
    ingest_reviews()