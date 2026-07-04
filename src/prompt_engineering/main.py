"""Main application entry point."""
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from prompt_engineering.api.router import router
from prompt_engineering.config.settings import get_settings

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="Prompt Engineering Patterns API", version="1.0.0")
    app.include_router(router)
    return app

app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("prompt_engineering.main:app", host=settings.api.host, port=settings.api.port, reload=settings.api.reload)
