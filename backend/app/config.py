from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "postgresql+psycopg://hanoihouse:hanoihouse@localhost:5432/hanoihouse"
    model_path: str = "ml_models/price_model_v1.joblib"
    cors_origins: list[str] = [
        "http://localhost:5500",
        "http://127.0.0.1:5501",
    ]


settings = Settings()