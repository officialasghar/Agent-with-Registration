from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from langchain.tools import tool


load_dotenv()

llama_api_key=os.getenv("OPENAI_API_KEY")
gemini_api_key=os.getenv("GEMINI_API_KEY")

# Use the permitted LLM model name

@tool
def get_any_answer(query:str):
    """Ask any question from this model"""
    llama_model = init_chat_model(
        model="llama-3.1-70b-instruct-awq",
        model_provider="openai",
        base_url="https://ai.infocare.sg/v1",
        api_key=llama_api_key
    )

    res=llama_model.invoke(query)

    return res