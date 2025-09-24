from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Learning Path Planner API"
    debug: bool = True
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    neo4j_url: str | None = None
    neo4j_user: str | None = None
    neo4j_password: str | None = None

settings = Settings()
