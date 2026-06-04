from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.ingredient import Ingredient
from app.schemas.ingredient import (
    IngredientCreate,
    IngredientUpdate,
    IngredientResponse
)
from app.security import get_current_user


router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredientes"]
)


@router.post("/", response_model=IngredientResponse)
def create_ingredient(
    ingredient_data: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ingredient = Ingredient(
        nombre=ingredient_data.nombre,
        cantidad=ingredient_data.cantidad,
        unidad=ingredient_data.unidad,
        usuario_id=current_user.id
    )

    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)

    return ingredient


@router.get("/", response_model=list[IngredientResponse])
def get_my_ingredients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Ingredient).filter(
        Ingredient.usuario_id == current_user.id
    ).all()


@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(
    ingredient_id: int,
    ingredient_data: IngredientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.usuario_id == current_user.id
    ).first()

    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado"
        )

    if ingredient_data.nombre is not None:
        ingredient.nombre = ingredient_data.nombre

    if ingredient_data.cantidad is not None:
        ingredient.cantidad = ingredient_data.cantidad

    if ingredient_data.unidad is not None:
        ingredient.unidad = ingredient_data.unidad

    db.commit()
    db.refresh(ingredient)

    return ingredient


@router.delete("/{ingredient_id}")
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.usuario_id == current_user.id
    ).first()

    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente no encontrado"
        )

    db.delete(ingredient)
    db.commit()

    return {
        "message": "Ingrediente eliminado correctamente"
    }