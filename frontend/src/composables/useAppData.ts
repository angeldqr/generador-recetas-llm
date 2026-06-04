import { computed, ref, type ComputedRef, type Ref } from 'vue'
import type { Ingredient, Recipe } from '../types/api'

const ingredients = ref<Ingredient[]>([])
const recipes = ref<Recipe[]>([])

export function useAppData() {
  const ingredientCount: ComputedRef<number> = computed(
    () => ingredients.value.length,
  )
  const recipeCount: ComputedRef<number> = computed(() => recipes.value.length)

  function setIngredients(next: Ingredient[]) {
    ingredients.value = next
  }

  function setRecipes(next: Recipe[]) {
    recipes.value = next
  }

  function prependRecipe(recipe: Recipe) {
    recipes.value = [
      recipe,
      ...recipes.value.filter((existing) => existing.id !== recipe.id),
    ]
  }

  function reset() {
    ingredients.value = []
    recipes.value = []
  }

  return {
    ingredients: ingredients as Ref<Ingredient[]>,
    recipes: recipes as Ref<Recipe[]>,
    ingredientCount,
    recipeCount,
    setIngredients,
    setRecipes,
    prependRecipe,
    reset,
  }
}
