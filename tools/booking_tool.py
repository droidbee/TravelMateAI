import requests
from langchain_core.tools import tool

from config.settings import DUFFEL_ACCESS_TOKEN


DUFFEL_ORDERS_URL = "https://api.duffel.com/air/orders"


@tool
def book_flight(
    offer_id: str,
    passenger_id: str,
    amount: str,
    currency: str,
    given_name: str,
    family_name: str,
    born_on: str,
    gender: str,
    title: str,
    email: str,
    phone_number: str,
) -> dict:
    """
    Book a selected Duffel flight offer.

    This is a consequential action and must only be called
    after explicit user approval.
    """

    normalized_gender = normalize_gender(gender)

    if normalized_gender is None:
        return {
        "success": False,
        "booking_created": False,
        "message": (
            "Invalid passenger gender. "
            "Please provide male, female, m, or f."
        ),
    }

    if not DUFFEL_ACCESS_TOKEN:
        return {
            "success": False,
            "booking_created": False,
            "message": "Duffel access token is not configured.",
        }

    headers = {
        "Authorization": f"Bearer {DUFFEL_ACCESS_TOKEN}",
        "Duffel-Version": "v2",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "data": {
            "type": "instant",
            "selected_offers": [
                offer_id,
            ],
            "payments": [
                {
                    "type": "balance",
                    "currency": currency,
                    "amount": amount,
                }
            ],
            "passengers": [
                {
                    "id": passenger_id,
                    "given_name": given_name,
                    "family_name": family_name,
                    "born_on": born_on,
                    "gender": normalized_gender,
                    "title": title,
                    "email": email,
                    "phone_number": phone_number,
                }
            ],
        }
    }

    try:
        response = requests.post(
            DUFFEL_ORDERS_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )

        if response.status_code != 201:
            return {
                "success": False,
                "booking_created": False,
                "status_code": response.status_code,
                "message": "Duffel booking request failed.",
                "error": response.text,
            }

        order = response.json()["data"]

        return {
            "success": True,
            "booking_created": True,
            "order_id": order["id"],
            "booking_reference": order.get("booking_reference"),
            "total_amount": order.get("total_amount"),
            "total_currency": order.get("total_currency"),
            "message": "Duffel test booking completed successfully.",
            "test_mode": True,
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "booking_created": False,
            "message": f"Duffel booking request failed: {error}",
        }

def normalize_gender(gender: str) -> str | None:
    value = gender.strip().lower()

    gender_map = {
        "m": "m",
        "male": "m",
        "f": "f",
        "female": "f",
    }

    return gender_map.get(value)