from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='./.env', env_file_encoding='utf-8')

    UPDATE_URL_MYDNS: str = ''
    UPDATE_URL_ALL: str = ''
    UPDATE_URL_SMTP: str = ''

@lru_cache()
def get_settings() -> Settings:
    return Settings()
