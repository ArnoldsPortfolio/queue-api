from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_secret: str = "queue-api-dev"
    database_url: str = "sqlite:///./queue_api.db"
    max_attempts: int = 3
    rate_per_minute: int = 30
