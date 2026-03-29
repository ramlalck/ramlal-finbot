from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str
    serpapi_api_key: str
    groq_model: str = "openai/gpt-oss-20b"
    sqlite_db_path: str = "/home/data/finance_agent.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


settings = Settings()
