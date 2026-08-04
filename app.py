from fastapi import FastAPI
from pydantic import BaseModel
from ai_service import ask_ai
import json

app = FastAPI()

with open("clinic_data.json", "r", encoding="utf-8") as file:
    clinic_data = json.load(file)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):

    reply = ask_ai(request.message, clinic_data)

    return {
        "reply": reply
    }