from fastapi import FastAPI
from models.schemas import ChatRequest, ChatResponse
from services.ai_service import ask_ai
import json

app = FastAPI(
    title="AI Clinic Assistant",
    version="2.0"
)

with open("data/clinic_data.json", "r", encoding="utf-8") as file:
    clinic_data = json.load(file)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    reply = ask_ai(
        session_id=request.session_id,
        message=request.message,
        clinic_data=clinic_data
    )

    return ChatResponse(
        reply=reply
    )