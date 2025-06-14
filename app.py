from fastapi import FastAPI, Request
from openai_agent import ask_chatbot

app = FastAPI()

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    user_input = body.get("message")
    reply = await ask_chatbot(user_input)
    return {"reply": reply}
