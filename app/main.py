from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.database import Base, engine
from app.models import User, Ingredient, Recipe, Rating
from app.routers import auth, ingredients, recipes
from app.config import settings


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Recetas LLM API",
    description="API para generar recetas con inventario usando inteligencia artificial",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS: restrict in production
origins = ["*"]
if settings.database_url and "localhost" not in settings.database_url:
    # In production, only allow the specific domain
    origins = [
        "https://recetasllm.online",
        "https://www.recetasllm.online",
        "http://localhost:5173",
        "http://localhost:3000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)

# Serve static files and favicon if they exist
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def root():
    return {
        "message": "API de Recetas LLM funcionando",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/favicon.ico")
def favicon():
    favicon_path = os.path.join(static_dir, "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return {"detail": "No favicon"}