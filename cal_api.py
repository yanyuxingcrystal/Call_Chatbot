import httpx
import os
from dotenv import load_dotenv

load_dotenv()
CAL_API_KEY = os.getenv("CALCOM_API_KEY")
BASE_URL = "https://api.cal.com/v1"

headers = {
    "Authorization": f"Bearer {CAL_API_KEY}",
    "Content-Type": "application/json"
}

async def book_meeting(email, date, time, reason):
    # you may need event_type_id or calendar_id for full implementation
    payload = {
        "email": email,
        "start": f"{date}T{time}:00Z",
        "title": reason
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE_URL}/bookings", json=payload, headers=headers)
        return r.json()

async def list_events(email):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/bookings?email={email}", headers=headers)
        return r.json()

async def cancel_event(email, datetime):
    # You'll need to find the event ID first based on email + datetime
    events = await list_events(email)
    match = next((e for e in events if datetime in e["startTime"]), None)
    if not match:
        return {"error": "No matching event found"}
    booking_id = match["id"]
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{BASE_URL}/bookings/{booking_id}", headers=headers)
        return {"status": r.status_code}

async def reschedule_event(email, old_datetime, new_datetime):
    events = await list_events(email)
    match = next((e for e in events if old_datetime in e["startTime"]), None)
    if not match:
        return {"error": "No matching event to reschedule"}
    booking_id = match["id"]
    payload = {"start": new_datetime}
    async with httpx.AsyncClient() as client:
        r = await client.patch(f"{BASE_URL}/bookings/{booking_id}", json=payload, headers=headers)
        return r.json()
