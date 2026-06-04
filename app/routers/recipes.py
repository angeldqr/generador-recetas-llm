from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.rating import Rating
from app.schemas.recipe import RecipeResponse, RatingCreate
from app.security import get_current_user
from app.services.llm_service import generate_recipe_from_inventory


router = APIRouter(
    prefix="/recipes",
    tags=["Recetas"]
)


@router.post("/generate", response_model=RecipeResponse)
def generate_recipe(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ingredientes = db.query(Ingredient).filter(
        Ingredient.usuario_id == current_user.id
    ).all()

    if not ingredientes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes registrar ingredientes antes de generar una receta"
        )

    try:
        recipe_data = generate_recipe_from_inventory(ingredientes)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando receta: {str(error)}"
        )

    recipe = Recipe(
        nombre_plato=recipe_data["nombre_plato"],
        ingredientes_json=recipe_data["ingredientes"],
        pasos_json=recipe_data["pasos"],
        tiempo_estimado=recipe_data["tiempo_estimado"],
        dificultad=recipe_data["dificultad"],
        usuario_id=current_user.id
    )

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe


@router.get("/", response_model=list[RecipeResponse])
def get_my_recipes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Recipe).filter(
        Recipe.usuario_id == current_user.id
    ).order_by(Recipe.fecha_creacion.desc()).all()


@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.usuario_id == current_user.id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receta no encontrada"
        )

    db.delete(recipe)
    db.commit()

    return {
        "message": "Receta eliminada correctamente"
    }


@router.post("/{recipe_id}/rate")
def rate_recipe(
    recipe_id: int,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.usuario_id == current_user.id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receta no encontrada"
        )

    existing_rating = db.query(Rating).filter(
        Rating.receta_id == recipe_id,
        Rating.usuario_id == current_user.id
    ).first()

    if existing_rating:
        existing_rating.estrellas = rating_data.estrellas

    else:
        new_rating = Rating(
            receta_id=recipe_id,
            usuario_id=current_user.id,
            estrellas=rating_data.estrellas
        )

        db.add(new_rating)

    db.commit()

    return {
        "message": "Receta calificada correctamente",
        "estrellas": rating_data.estrellas
    }