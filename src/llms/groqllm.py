from pyexpat import model
from langchain.chains import llm
from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv

class GroqLLM:
    def __init__(self):
        load_dotenv()
        self.groq_api_key=os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is missing from .env")
        
        
    def get_llm(self,model="llama-3.3-70b-versatile"):    
        try:
            return ChatGroq(api_key=self.groq_api_key, model=model) # pyright: ignore[reportArgumentType]
        except Exception as e:
            raise RuntimeError(f"Failed to initialize ChatGroq: {e}")