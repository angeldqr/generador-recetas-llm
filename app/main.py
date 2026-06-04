from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from app.database import Base, engine
from app.models import User, Ingredient, Recipe, Rating
from app.routers import auth, ingredients, recipes


def create_database_tables() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except (OperationalError, UnicodeDecodeError) as error:
        raise RuntimeError(
            "No se pudo conectar a PostgreSQL. Revisa DATABASE_URL en .env "
            "y confirma que la base generador-recetas-llm-db exista."
        ) from error


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_tables()
    yield


app = FastAPI(
    title="Recetas LLM API",
    description="API para generar recetas con inventario usando inteligencia artificial",
    version="1.0.0",
    lifespan=lifespan
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
