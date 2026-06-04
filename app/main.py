from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import User, Ingredient, Recipe, Rating
from app.routers import auth, ingredients, recipes


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Recetas LLM API",
    description="API para generar recetas con inventario usando inteligencia artificial",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)


@app.get("/")
def root():
    return {
        "message": "API de Recetas LLM funcionando"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }