from fastapi import FastAPI
from app.api.v1.endpoints import Message, router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.language_processing import detect_intent_spacy,extract_entities_spacy 
from pydantic import BaseModel
import spacy

app = FastAPI()

#Load the spaCy model
nlp = spacy.load("en_core_web_sm")

class Message(BaseModel):
    user_message:str
    
#Simple conversation state tracking
conversation_state = {}

app.include_router(chat_router,prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/chat")
async def chat(message: Message):
    
    user_id = 123
    user_message = message.user_message
    intent = detect_intent_spacy(user_message)
   
    #Track conversation state
    if user_id not in conversation_state:
       conversation_state[user_id] = {}
       
    # Intent handling logic
    if intent == "transfer_money":
        if "account_number" not in conversation_state[user_id]:
            #First step:
            conversation_state[user_id]["intent"]="transfer_money"
            conversation_state[user_id]["account_number"]=extract_entities_spacy(user_message)["account_number"]
            return {"response":"How much would you like to transfer?"}
        else:
            amount = extract_entities_spacy(user_message)["amount"]
            conversation_state[user_id]["amount"]=amount
            return {"response":f"Transfering {amount} from account {conversation_state[user_id]['account_number']}."}
    else :
        return {"response":"I'm sorry, I didn't understand your request."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)