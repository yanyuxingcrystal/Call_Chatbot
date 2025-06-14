from fastapi import FastAPI, Request
from openai_agent_1 import ask_chatbot
# from openai_agent_2 import chat_with_functions
import os
from dotenv import load_dotenv

load_dotenv()

print("🔥 CAL_API_KEY in app.py:", os.getenv("CAL_API_KEY"))
print("🔥 OPENAI_API_KEY in app.py:", os.getenv("OPENAI_API_KEY"))

app = FastAPI()

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    user_input = body.get("message")
    reply = await ask_chatbot(user_input)
    return {"reply": reply}
