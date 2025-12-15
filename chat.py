import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

GROQ_KEY = os.environ.get("GROQ_API_KEY")

@app.post("/api/chat")
async def chat_with_groq(req: Request):
    body = await req.json()
    user_msg = body.get("message", "")

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_msg}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    result = response.json()
    reply = result["choices"][0]["message"]["content"]

    return JSONResponse({"reply": reply})
