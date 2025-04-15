from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    FIREBIRD_HOST: str = "localhost"
    FIREBIRD_DATABASE: str = "database.fdb"
    FIREBIRD_USER: str = "SYSDBA"
    FIREBIRD_PASSWORD: str = "masterkey"
    FIREBIRD_PORT: int = 3050
    FIREBIRD_CHARSET: str = "UTF8"
    API_USERNAME: str = "admin"
    API_PASSWORD: str = "admin"
    MCP_DATABASE_URL: str = "sqlite:///./mcp.db"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()