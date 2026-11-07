from anyio.functools import lru_cache
from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "My API"
    app_version: str = "0.0.1"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version)

@app.get("/")
async def root():
    return {"app": settings.app_name,"version": settings.app_version}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
