from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My App"
    celery_broker_url: str
    celery_result_backend: str

    class Config:
        env_file = ".env"

settings = Settings()
