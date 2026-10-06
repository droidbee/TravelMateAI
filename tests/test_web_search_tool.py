from tools.web_search_tool import search_web


result = search_web.invoke(
    {
        "query": "latest travel disruptions in Sharjah"
    }
)

print("\nWeb search result:")
print(result)