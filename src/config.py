from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT: str
    AZURE_OPENAI_API_VERSION: str = "2025-04-01-preview"
    AZURE_OPENAI_API_KEY: str

    # Embeddings
    EMBEDDING_ENDPOINT: str
    EMBEDDING_DEPLOYMENT: str
    EMBEDDING_API_VERSION: str = "2024-12-01-preview"

    # Search
    SEARCH_ENDPOINT: str
    SEARCH_INDEX: str
    SEARCH_API_VERSION: str = "2024-07-01"
    SEARCH_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
