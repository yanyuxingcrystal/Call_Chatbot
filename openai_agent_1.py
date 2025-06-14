import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from cal_api_sync import book_meeting, list_events, cancel_event, reschedule_event

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"✅ DEBUG: OpenAI_API Key is: {api_key}")

client = OpenAI(api_key=api_key)

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

def ask_chatbot(user_input: str, user_email: str = None):
    messages = [{"role": "user", "content": user_input}]
    if user_email:
        messages.append({"role": "system", "content": f"User email is {user_email}."})

    try:
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call="auto"
        )
        choice = chat.choices[0].message

        if choice.function_call:
            func_name = choice.function_call.name
            args_str = choice.function_call.arguments
            try:
                args = json.loads(args_str)
            except Exception as e:
                return f"❌ file to load json: {e}"

            # 补全 email
            if "email" in functions_dict[func_name]["parameters"]["properties"].keys() and "email" not in args:
                if user_email:
                    args["email"] = user_email
                else:
                    return "⚠️ Please enter your email."

            if func_name == "book_meeting":
                result = book_meeting(**args)  # 同步调用
                return f"✅ Meeting has been booked!：{result}"
            elif func_name == "list_events":
                result = list_events(**args)
                return f"📅 Your Meeting List: ：{result}"
            elif func_name == "cancel_event":
                result = cancel_event(**args)
                return "✅ Meeting has been cancelled!"
            elif func_name == "reschedule_event":
                result = reschedule_event(**args)
                return "✅ Meeting has been rescheduled!"
            else:
                return f"⚠️ Unknown function call：{func_name}"

        if choice.content:
            return choice.content
        return "🤖 No Content"
    except Exception as e:
        return f"🔥 OpenAI API failed: {str(e)}"



# 用于根据函数名快速查参数定义
functions_dict = {f["name"]: f for f in functions}
