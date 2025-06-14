import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from cal_api import book_meeting, list_events, cancel_event, reschedule_event

# 加载环境变量
load_dotenv()
# 获取 OpenAI Key（你必须配置 .env 文件或环境变量）
api_key = os.getenv("OPENAI_API_KEY")

# ✅ 创建 OpenAI 客户端
client = OpenAI(api_key=api_key)
# openai.api_key = os.getenv("OPENAI_API_KEY")

functions = [
    {
        "name": "book_meeting",
        "description": "Create a meeting on Cal.com",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "date": {"type": "string"},
                "time": {"type": "string"},
                "reason": {"type": "string"}
            },
            "required": ["email", "date", "time", "reason"]
        }
    },
    {
        "name": "list_events",
        "description": "List user's events",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string"}
            },
            "required": ["email"]
        }
    },
    {
        "name": "cancel_event",
        "description": "Cancel an event",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "datetime": {"type": "string"}
            },
            "required": ["email", "datetime"]
        }
    },
    {
        "name": "reschedule_event",
        "description": "Reschedule a meeting",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "old_datetime": {"type": "string"},
                "new_datetime": {"type": "string"}
            },
            "required": ["email", "old_datetime", "new_datetime"]
        }
    }
]


async def ask_chatbot(user_input):
    # chat = openai.ChatCompletion.create(
    #     model="gpt-4-0613",
    #     messages=[{"role": "user", "content": user_input}],
    #     functions=functions,
    #     function_call="auto"
    # )
    chat = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}],
        functions=functions,
        function_call="auto"
    )

    # response = response.choices[0].message.content
    response = chat.choices[0].message.content

    if response.get("function_call"):
        func_name = response["function_call"]["name"]
        args = eval(response["function_call"]["arguments"])

        if func_name == "book_meeting":
            return await book_meeting(**args)
        elif func_name == "list_events":
            return await list_events(**args)
        elif func_name == "cancel_event":
            return await cancel_event(**args)
        elif func_name == "reschedule_event":
            return await reschedule_event(**args)

    return response["content"]
