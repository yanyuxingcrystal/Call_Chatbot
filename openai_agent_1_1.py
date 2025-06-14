# import openai
# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# from cal_api import book_meeting, list_events, cancel_event, reschedule_event

import openai
from openai import OpenAI

import json
from pathlib import Path
from dotenv import load_dotenv
import os
from cal_api import book_meeting, list_events, cancel_event, reschedule_event

# 加载环境变量
# dotenv_path = Path(__file__).resolve().parent / ".env"
# load_dotenv(dotenv_path)
load_dotenv()

# 获取 OpenAI Key（你必须配置 .env 文件或环境变量）
api_key = os.getenv("OPENAI_API_KEY") # type: ignore
print(f"✅ DEBUG: API Key is: {api_key}")

# ✅ 创建 OpenAI 客户端
client = OpenAI(api_key=api_key)
# openai.api_key = os.getenv("OPENAI_API_KEY")
print("✅ Loaded API KEY:", api_key)

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
    # chat = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": user_input}],
    #     functions=functions,
    #     function_call="auto"
    # )
    try:
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 明确指定支持 functions 的版本
            messages=[{"role": "user", "content": user_input}],
            functions=functions,
            function_call="auto"
        )
        # response = response.choices[0].message.content
        # response = chat.choices[0].message.content
        choice = chat.choices[0]
        message = choice.message
        # ✅ 处理 function call 请求
        # if hasattr(message, "function_call") and message.function_call:
        #     func_name = message.function_call.name
        #     args_str = message.function_call.arguments
        #     try:
        #         args = json.loads(args_str)  # 推荐用 json 而不是 eval，更安全
        #     except Exception as e:
        #         return f"❌ 参数解析失败: {e}"
        #
        #     if func_name == "book_meeting":
        #         return await book_meeting(**args)
        #     elif func_name == "list_events":
        #         return await list_events(**args)
        #     elif func_name == "cancel_event":
        #         return await cancel_event(**args)
        #     elif func_name == "reschedule_event":
        #         return await reschedule_event(**args)
        #     else:
        #         return f"⚠️ 未知函数调用: {func_name}"
        #
        # # ✅ 普通回答内容
        # return message.content if message.content else "🤖 没有返回内容。"

    except Exception as e:
        return f"🔥 OpenAI API 调用失败: {str(e)}"

    # if response and response.get("function_call"):
    #     func_name = response["function_call"]["name"]
    #     args = eval(response["function_call"]["arguments"])
    #
    #     if func_name == "book_meeting":
    #         return await book_meeting(**args)
    #     elif func_name == "list_events":
    #         return await list_events(**args)
    #     elif func_name == "cancel_event":
    #         return await cancel_event(**args)
    #     elif func_name == "reschedule_event":
    #         return await reschedule_event(**args)
    #
    # return response["content"]
