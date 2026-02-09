from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    openrouter_api_key: SecretStr
    google_chat_webhook_url: SecretStr

    model_name: str = "perplexity/sonar-pro-search"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
