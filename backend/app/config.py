from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    QDRANT_URL: str
    QDRANT_API_KEY: str
    GEMINI_API_KEY: str
    COLLECTION_NAME: str = "knowledge_base"
    CHUNK_SIZE: int = 460
    CHUNK_OVERLAP: int = 80
    TOP_K: int = 10
    SCORE_THRESHOLD: float = 0.0

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(env_file=".env")

settings = Settings()