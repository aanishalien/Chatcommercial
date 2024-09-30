from fastapi import APIRouter
from pydantic import BaseModel
from app.core.language_processing import detect_language
from app.services.chatbot_service import generate_chatbot_response
import openai
from app.core.config import settings
router =APIRouter()

class Message (BaseModel):
    user_message: str
    
@router.post("/chat")
async def chat(message:Message):
    language = detect_language(message.user_message)
    response = generate_chatbot_response(message.user_message)
    return{"response":response}

#async def process_user_message(user_message:str)-> str:
    """
    Process user message and return chatbot's response using OpenAI API.
    """
    openai.api.key = settings.OPENAI_API_KEY
    
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=user_message,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return "Sorry,I encountered an error processing your message."