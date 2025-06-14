from pydantic import BaseModel

class BookMeetingParams(BaseModel):
    email: str
    date: str  # e.g. 2025-06-13
    time: str  # e.g. 15:00
    reason: str

class ListEventsParams(BaseModel):
    email: str

class CancelEventParams(BaseModel):
    email: str
    datetime: str  # ISO format

class RescheduleEventParams(BaseModel):
    email: str
    old_datetime: str
    new_datetime: str
