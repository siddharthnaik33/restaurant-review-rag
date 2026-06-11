from tools import review_retriever

print("Restaurant Review Search Assistant Started")
print("Type exit to stop")

while True:
    query = input("\nAsk: ")

    if query.lower() == "exit":
        break

    result = review_retriever.invoke(query)

    print("\nAnswer based on restaurant reviews:")
    print(result)