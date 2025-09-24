from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    environment: str = Field(default="dev")
    database_url: str = Field(default="sqlite:///./data.db")
    mastery_threshold_default: float = Field(default=0.8)
    openai_api_key: str | None = Field(default=None)
    openai_model: str = Field(default="gpt-4o-mini")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()