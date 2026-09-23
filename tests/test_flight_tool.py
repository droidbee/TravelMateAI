from tools.flight_tool import search_flights


result = search_flights.invoke(
    {
        "origin": "DXB",
        "destination": "LHR",
        "departure_date": "2026-10-21",
        "adults": 1,
    }
)

print("\nFlight search result:")
print(result)