from pydantic import BaseModel

class Message(BaseModel):
    user_message:str

    
class Response(BaseModel):
    response:str