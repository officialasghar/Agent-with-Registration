from langchain.chat_models import init_chat_model
from app.settings import settings


llama_api_key=settings.OPENAI_API_KEY
gemini_api_key=settings.GEMINI_API_KEY

# Use the permitted LLM model name
llama_model = init_chat_model(
    model="llama-3.1-70b-instruct-awq",
    model_provider="openai",
    base_url="https://ai.infocare.sg/v1",
    api_key=llama_api_key
)


gemini_model = init_chat_model(
    model="gemini-3.5-flash-lite",
    model_provider="google_genai",
    api_key=gemini_api_key
)