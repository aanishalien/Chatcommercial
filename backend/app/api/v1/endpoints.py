from fastapi import APIRouter
from pydantic  import BaseModel
from app.core.language_processing import detect_language, generate_response
from .schemas import Message
from app.core.language_processing import detect_intent_spacy,extract_entities_spacy,load_dataset

router = APIRouter()

dataset = load_dataset()

class Message(BaseModel):
    user_message:str
    
#Simple conversation state tracking
conversation_state={}

#Hotline number
HOTLINE_NUMBER = "1-800-435-9303"

    
@router.post("/chat")
async def chat(message:Message):
    user_id=123
    user_message=message.user_message
    intent =detect_intent_spacy(user_message)
    
    #Check if the user mentions account issues
    if "account issue" in user_message.lower():
        return {"response":f"For account issues, please contact out hotlines at {HOTLINE_NUMBER}."}
    
    if user_id not in conversation_state:
        conversation_state[user_id]={}
        
    if intent == "transfer_money":
        if "account_number" not in conversation_state[user_id]:
            conversation_state[user_id]["intent"]="transfer_money"
            conversation_state[user_id]["account_number"]=extract_entities_spacy(user_message)["account_number"]
            return {"response":"How much would you like to transfer?"}
        
        else:
            #Process the next step
            amount = extract_entities_spacy(user_message)["amount"]
            conversation_state[user_id]["amount"]=amount
            return {"response":f"Transfering{amount}."}
    # DataSet-based on the response
    for entry in dataset:
        if entry['input'].lower() == user_message.lower():
            return {"response":entry['response']}
        
    return {"response":"I couldn't understand your request."}