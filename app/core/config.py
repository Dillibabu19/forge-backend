from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    class Config:
        extra='ignore'
        env_file = ".env"

settings = Settings()