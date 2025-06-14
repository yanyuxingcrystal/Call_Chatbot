from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from openai_agent_1 import ask_chatbot

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    user_email: str = None

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    reply = ask_chatbot(req.message, req.user_email)
    return {"reply": reply}
