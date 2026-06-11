from tools import review_retriever

query = "best biryani in Hyderabad"

result = review_retriever.invoke(query)

print(result)