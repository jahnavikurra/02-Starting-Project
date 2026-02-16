from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Azure OpenAI settings
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = ""
    AZURE_OPENAI_API_VERSION: str = "2025-04-01-preview"

    # Embedding settings
    EMBEDDING_ENDPOINT: str = ""
    EMBEDDING_DEPLOYMENT: str = ""
    EMBEDDING_API_VERSION: str = "2024-12-01-preview"

    # Search settings
    SEARCH_ENDPOINT: str = ""
    SEARCH_INDEX: str = ""
    SEARCH_API_VERSION: str = "2024-07-01"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
