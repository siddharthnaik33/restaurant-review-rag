from agent import create_restaurant_agent

agent = create_restaurant_agent()

print("Restaurant Review Assistant Started")
print("Type exit to stop")

while True:
    query = input("\nAsk: ")

    if query.lower() == "exit":
        break

    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    print("\nAnswer:")
    print(response["messages"][-1].content)