from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    model_config = ConfigDict(env_file=".env", env_file_encoding='utf-8')

# Única instancia que será usada en toda la app
settings = Settings()