from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_env: str = "prod"

    db_name: str
    db_schema: str
    db_username: str
    db_host: str
    db_port: int = 5432
    db_password: str | None = None

    rag_service_url: str = None
    frontend_url: str = ""

    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str
    smtp_password: str
    mail_sender: str


def load_config() -> Settings:
    return Settings()
