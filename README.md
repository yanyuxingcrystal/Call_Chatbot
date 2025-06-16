## Features
- Book,List,Cancel,Reschedule appointment from Cal.com API
- Uses OpenAI Assistant to process the input content to choose which intent it will be
## Setup
1. Clone the repository
2. Set up your environment variables in Replit Secrets:
   - `OPENAI_API_KEY`
   - `CAL_API_KEY_3`
3. Install dependencies:
   ```
   pip install openai requests
   ```
## service run
uvicorn app:app --reload
## test call
```
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me book a meeting tomorrow at 3pm for project discussion", "user_email": "xxx@gmail.com"}'
```
