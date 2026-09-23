import requests
from langchain_core.tools import tool


from config.settings import DUFFEL_API_URL, DUFFEL_ACCESS_TOKEN


@tool
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    adults: int = 1,
) -> dict:
    """
    Search for one-way flights.

    Args:
        origin: Origin airport IATA code, for example DXB.
        destination: Destination airport IATA code, for example LHR.
        departure_date: Departure date in YYYY-MM-DD format.
        adults: Number of adult passengers.

    Returns:
        A dictionary containing matching flight offers.
    """

    

    if not DUFFEL_ACCESS_TOKEN:
        return {
            "found": False,
            "flights": [],
            "message": "Duffel access token is not configured.",
        }

    headers = {
        "Authorization": f"Bearer {DUFFEL_ACCESS_TOKEN}",
        "Duffel-Version": "v2",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "data": {
            "slices": [
                {
                    "origin": origin.upper(),
                    "destination": destination.upper(),
                    "departure_date": departure_date,
                }
            ],
            "passengers": [
                {"type": "adult"}
                for _ in range(adults)
            ],
            "cabin_class": "economy",
        }
    }

    response = requests.post(
        DUFFEL_API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    if response.status_code != 201:
        return {
            "found": False,
            "flights": [],
            "message": "Flight search failed.",
            "status_code": response.status_code,
        }

    data = response.json()["data"]
    offers = data.get("offers", [])

    if not offers:
        return {
            "found": False,
            "flights": [],
            "message": "No matching flights were found.",
        }

    flights = []

    # Keep only a few offers for the LLM.
    for offer in offers[:5]:
        flight_slice = offer["slices"][0]
        segments = flight_slice["segments"]

        first_segment = segments[0]
        last_segment = segments[-1]

        airline = first_segment["marketing_carrier"]

        flight_segments = []

        for segment in segments:
            carrier = segment["marketing_carrier"]
            flight_segments.append(
                {
                    "airline": carrier["name"],
                    "flight_number": carrier["iata_code"]
                    + segment["marketing_carrier_flight_number"],
                     "origin": segment["origin"]["iata_code"],
                      "destination": segment["destination"]["iata_code"],
                     "departure": segment["departing_at"],
                    "arrival": segment["arriving_at"],
             }
            )

        flights.append(
            {
                "offer_id": offer["id"],
                "airline": airline["name"],
                "flight_number": (
                    airline["iata_code"]
                    + first_segment[
                        "marketing_carrier_flight_number"
                    ]
                ),
                "origin": flight_slice["origin"]["iata_code"],
                "destination": flight_slice["destination"]["iata_code"],
                "departure": first_segment["departing_at"],
                "arrival": last_segment["arriving_at"],
                "duration": flight_slice["duration"],
                "stops": len(segments) - 1,
                "segments": flight_segments,
                "price": offer["total_amount"],
                "currency": offer["total_currency"],
            }
        )

    return {
        "found": True,
        "flights": flights,
        "message": f"Found {len(offers)} flight offers.",
        "test_mode": True,
    }