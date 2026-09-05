import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "CanonGuard AI"
    VERSION: str = "1.0.0"
    UNIVERSE_ID: str = "CHRONOVERSE"
    
    # ClickHouse Connection Details
    CLICKHOUSE_HOST: str = os.getenv("CLICKHOUSE_HOST", "localhost")
    CLICKHOUSE_PORT: int = int(os.getenv("CLICKHOUSE_PORT", "8123"))
    CLICKHOUSE_USER: str = os.getenv("CLICKHOUSE_USER", "default")
    CLICKHOUSE_PASSWORD: str = os.getenv("CLICKHOUSE_PASSWORD", "")
    CLICKHOUSE_DATABASE: str = os.getenv("CLICKHOUSE_DATABASE", "canonguard")
    CLICKHOUSE_SECURE: bool = os.getenv("CLICKHOUSE_SECURE", "false").lower() in ("true", "1")
    
    # Gemini / Google ADK API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Engine Settings
    DEBOUNCE_MS: int = 350
    STRICT_MODE: bool = True

settings = Settings()
