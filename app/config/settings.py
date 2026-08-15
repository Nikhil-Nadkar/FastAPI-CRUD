from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    Database_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRY: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
