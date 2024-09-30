import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_KEY_KEY = os.getenv("OPENAI_API_KEY")
    OTHER_SETTING = os.getenv("OTHER_SETTING","default_value")