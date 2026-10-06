from tools.flight_tool import search_flights
from tools.booking_tool import book_flight


print("\n--- SEARCHING FOR FRESH FLIGHT OFFER ---")

search_result = search_flights.invoke(
    {
        "origin": "DXB",
        "destination": "LHR",
        "departure_date": "2026-10-21",
        "adults": 1,
    }
)


if not search_result["found"]:
    print("Flight search failed:")
    print(search_result)
    raise SystemExit


flight = search_result["flights"][0]

print("\nSelected flight:")
print("Airline:", flight["airline"])
print("Flight:", flight["flight_number"])
print("Offer ID:", flight["offer_id"])
print("Price:", flight["price"], flight["currency"])
print("Expires:", flight["expires_at"])
print("Passenger:", flight["passengers"][0]["id"])


print("\n--- CREATING DUFFEL TEST BOOKING ---")

booking_result = book_flight.invoke(
    {
        "offer_id": flight["offer_id"],
        "passenger_id": flight["passengers"][0]["id"],
        "amount": flight["price"],
        "currency": flight["currency"],

        # Fictional test passenger
        "given_name": "Test",
        "family_name": "Traveller",
        "born_on": "1990-01-01",
        "gender": "m",
        "title": "mr",
        "email": "test@example.com",
        "phone_number": "+442080160000",
    }
)


print("\nBooking result:")
print(booking_result)