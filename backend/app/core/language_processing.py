from unittest import result
import spacy
from langdetect import detect
from transformers import pipeline
import json

#Load spaCy's English model
nlp_spacy = spacy.load("en_core_web_sm")

def load_dataset():
    with open('app/data/dataset.json',encoding='utf-8') as f:
        return json.load(f)

def detect_intent_spacy(user_message):
    doc = nlp_spacy(user_message)

    #For simple intent classification,you can check for keywords
    if "balance" in user_message.lower():
        return "check_balance"
    elif "transfer" in user_message.lower():
        return "transfer_money"
    else:
        return "unknown_intent"
    
def extract_entities_spacy(user_message):
    doc = nlp_spacy(user_message)
    
    #For extracting entities,you can use spaCy's entity recognition
    entities = {"account_number":None,"amount":None}
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            entities["amount"]=ent.text
        elif ent.label_ == "CARDINAL":
            entities["account_number"]=ent.text
            
    return entities

#Load the transformers model
nlp_transformers = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def detect_intent_transformers(user_message):
    candidate_labels = ["check_balance","transfer_money","loan_request","unknown"]
    nlp_transformers(user_message,candidate_labels)
    return result['labels'][0]


def detect_language(text: str) -> str:
    
    if "hello" in text.lower() or "ayubowen" in text.lower():
        return "en"
    elif "සිංහල" in text:
        return "si"
    elif "தமிழ்" in text:
        return "ta"
    else:
        return "sg"

def generate_response(language: str, user_message: str) -> str:
    # A dictionary to map responses for different languages
    responses = {
        "en": "This is a response in English",
        "si": "මෙය සිංහලෙන් ප්‍රතිචාරයකි",
        "ta": "இது தமிழ் பதில் ஆகும்",
        "sg": "This is a response in Singlish",
    }
    return responses.get(language, "Sorry, I don't understand the language")

def process_message(user_message:str) -> str:
    response = f"Chatbot recieved:{user_message}"
    return response
