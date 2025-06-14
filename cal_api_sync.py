
from dotenv import load_dotenv
import os
import requests

load_dotenv()
CAL_API_KEY = os.getenv("CAL_API_KEY_3")
BASE_URL = "https://api.cal.com/v1"

# BASE_URL = "https://api.cal.com/v1?apikey={CAL_API_KEY}"
print("🔑 CAL_API_KEY =", CAL_API_KEY)

# headers = {
#     "Authorization": f"Bearer {CAL_API_KEY}",
#     "Content-Type": "application/json"
# }
headers = {
    "x-api-key": "{CAL_API_KEY}",
    "Content-Type": "application/json"
}
def book_meeting(email, date, time, reason):
    payload = {
        "eventTypeId": "evt_abc123",
        "start": "2025-06-15T22:00:00Z",
        "invitee": {
            "email": "yanyuxingcrystal@gmail.com",
            "name": "Crystal Yan"
        },
        "title": "Project Discussion",
        "location": "Zoom"
    }

    response = requests.post(f"{BASE_URL}/bookings", json=payload, headers=headers)
    return response.json()


def list_events(email):
    response = requests.get(f"{BASE_URL}/bookings?email={email}", headers=headers)
    return response.json()


def cancel_event(email, datetime):
    events = list_events(email)
    match = next((e for e in events if datetime in e["startTime"]), None)

    if not match:
        return {"error": "No matching event found"}

    booking_id = match["id"]
    response = requests.delete(f"{BASE_URL}/bookings/{booking_id}", headers=headers)
    return {"status": response.status_code}

def reschedule_event(email, old_datetime, new_datetime):
    events = list_events(email)
    match = next((e for e in events if old_datetime in e["startTime"]), None)

    if not match:
        return {"error": "No matching event to reschedule"}

    booking_id = match["id"]
    payload = {"start": new_datetime}
    response = requests.patch(f"{BASE_URL}/bookings/{booking_id}", json=payload, headers=headers)
    return response.json()
