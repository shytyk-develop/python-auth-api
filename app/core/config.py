from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "FastAPI Auth API"
    api_v1_prefix: str = ""

    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_exp_minutes: int = 60 * 24

    cookie_name: str = "access_token"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_from_name: str = "FastAPI Auth API"
    admin_username: str = ""
    admin_password: str = ""


settings = Settings()
