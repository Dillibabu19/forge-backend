from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    class Config:
        extra='ignore'
        env_file = ".env"

settings = Settings()