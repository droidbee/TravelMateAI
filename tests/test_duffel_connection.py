import os
from datetime import date, timedelta

import requests
from dotenv import load_dotenv


load_dotenv()

DUFFEL_ACCESS_TOKEN = os.getenv("DUFFEL_ACCESS_TOKEN")

url = "https://api.duffel.com/air/offer_requests"

headers = {
    "Authorization": f"Bearer {DUFFEL_ACCESS_TOKEN}",
    "Duffel-Version": "v2",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

departure_date = (date.today() + timedelta(days=30)).isoformat()

payload = {
    "data": {
        "slices": [
            {
                "origin": "DXB",
                "destination": "LHR",
                "departure_date": departure_date,
            }
        ],
        "passengers": [
            {
                "type": "adult"
            }
        ],
        "cabin_class": "economy",
    }
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60,
)

print("Status code:")
print(response.status_code)

print("\nResponse:")
data = response.json()

print("\nResponse keys:")
print(data.keys())

if response.status_code == 201:
    offer_request = data["data"]

    print("\nOffer Request ID:")
    print(offer_request["id"])

    offers = offer_request.get("offers", [])

    print("\nNumber of offers:")
    print(len(offers))

    if offers:
        first_offer = offers[0]

        print("\nFirst offer:")
        print("Offer ID:", first_offer["id"])
        print("Total amount:", first_offer["total_amount"])
        print("Currency:", first_offer["total_currency"])

        slices = first_offer["slices"]

        print("\nNumber of slices:")
        print(len(slices))

        first_slice = slices[0]

        print("\nSlice:")
        print("Origin:", first_slice["origin"]["iata_code"])
        print("Destination:", first_slice["destination"]["iata_code"])
        print("Duration:", first_slice["duration"])

        segments = first_slice["segments"]

        print("\nNumber of segments:")
        print(len(segments))

        for index, segment in enumerate(segments, start=1):
            print(f"\nSegment {index}:")
            print(
                "From:",
                segment["origin"]["iata_code"],
            )
            print(
                "To:",
                segment["destination"]["iata_code"],
            )
            print(
                "Departure:",
                segment["departing_at"],
            )
            print(
                "Arrival:",
                segment["arriving_at"],
            )
            print(
                "Airline:",
                segment["marketing_carrier"]["name"],
            )
            print(
                "Flight number:",
                segment["marketing_carrier"]["iata_code"]
                + segment["marketing_carrier_flight_number"],
            )
else:
    print("\nError response:")
    