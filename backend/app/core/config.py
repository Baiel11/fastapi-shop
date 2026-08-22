from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Shop"
    debug: bool = True
    database_url: str = "postgresql://fashop_admin:fashop_secure_password@localhost:5432/fashop_db"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    static_dir: str = "static"
    images_dir: str = "static/images"

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    reset_token_expire_minutes: int = 30
    frontend_url: str = "http://localhost:5173"

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    email_from: str | None = None

    @property
    def smtp_configured(self) -> bool:
        return bool(self.smtp_user and self.smtp_password)

    refresh_cookie_name: str = "refresh_token"
    refresh_cookie_path: str = "/api/auth"
    cookie_samesite: str = "lax"

    class Config:
        env_file = (".env", "../.env")
        extra = "ignore"

settings = Settings()
