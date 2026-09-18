import json
from models.schemas import Destination
from pathlib import Path
from langchain_core.tools import tool

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "destinations.json"


@tool
def search_destinations(country: str | None = None, interest: str | None = None) -> dict:
    """Search travel destinations by country and travel interest.

    Use this tool when the user is looking for travel destinations
    matching a country and/or an interest such as relaxing, scenic,
    historical, food, adventure, or cultural experiences.
    """

    with open(DATA_PATH, "r") as f:
        data = json.load(f)


    destinations = [Destination(**dest) for dest in data]

    results = destinations

    if country:
        country_lower = country.lower()
        results = [
            dest for dest in results if dest.country.lower() == country_lower
        ]

    if interest:
        interest_lower = interest.lower()
        results = [
            dest
            for dest in results
            if interest_lower in [value.lower() for value in dest.best_for]
            or interest_lower in [value.lower() for value in dest.type]
        ]

    count = len(results)
    label = "destination" if count == 1 else "destinations"

    if not results:
        return {
            "found": False,
            "destinations": [],
            "message": "No matching destinations were found."
        }
    

    return {
        "found": True,
        "destinations": [
        destination.model_dump()
        for destination in results
        ],
        "message": f"Found {len(results)} matching {label}."
}

