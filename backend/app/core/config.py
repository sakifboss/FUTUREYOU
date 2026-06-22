from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FutureYou API"
    environment: str = "development"
    database_url: str = "sqlite:///./futureyou.db"
    backend_cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    llm_provider: str = "mock"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:3b"
    openai_compatible_base_url: str | None = None
    openai_compatible_api_key: str | None = None
    openai_compatible_model: str | None = None

    embedding_dimensions: int = Field(default=256, ge=64, le=4096)
    rag_top_k: int = Field(default=5, ge=1, le=12)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
