from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    OPENAI_API_KEY: str
    GEMINI_API_KEY: str

    WEATHER_API_KEY: str

    LANGSMITH_TRACING: bool
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str

    USER_DATABASE_URL: str
    AGENT_DB_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
