from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cache_expire: int = 300  # default value of 300 if CACHE_EXPIRE is not set

    class Config:
        env_prefix = "QA_"
        env_file = ".env"


settings = Settings()
