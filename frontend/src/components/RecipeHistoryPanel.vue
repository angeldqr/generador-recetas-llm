<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { deleteRecipe, getRecipes, rateRecipe } from '../services/api'
import type { Recipe } from '../types/api'

const props = defineProps<{
  token: string
}>()

const emit = defineEmits<{
  loaded: [recipes: Recipe[]]
  open: [recipe: Recipe]
}>()

const recipes = ref<Recipe[]>([])
const isLoading = ref(false)
const busyRecipeId = ref<number | null>(null)
const errorMessage = ref('')
const successMessage = ref('')

function publishRecipes(nextRecipes: Recipe[]) {
  recipes.value = nextRecipes
  emit('loaded', nextRecipes)
}

function openRecipe(recipe: Recipe) {
  emit('open', recipe)
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat('es-CO', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(new Date(value))
}

async function loadRecipes() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    publishRecipes(await getRecipes(props.token))
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo cargar el historial.'
  } finally {
    isLoading.value = false
  }
}

async function removeRecipe(recipe: Recipe) {
  busyRecipeId.value = recipe.id
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await deleteRecipe(recipe.id, props.token)
    successMessage.value = `${recipe.nombre_plato} eliminado del historial.`
    await loadRecipes()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo eliminar la receta.'
  } finally {
    busyRecipeId.value = null
  }
}

async function submitRating(recipe: Recipe, stars: number) {
  busyRecipeId.value = recipe.id
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await rateRecipe(recipe.id, stars, props.token)
    successMessage.value = `${recipe.nombre_plato} calificada con ${stars} estrellas.`
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo calificar la receta.'
  } finally {
    busyRecipeId.value = null
  }
}

onMounted(loadRecipes)
</script>

<template>
  <section class="history-panel" aria-labelledby="history-title">
    <div class="history-panel__header">
      <div>
        <p class="workspace__label">Historial</p>
        <h2 id="history-title">Recetas guardadas</h2>
      </div>
      <button class="pill-button pill-button--light" type="button" @click="loadRecipes">
        Actualizar
      </button>
    </div>

    <p v-if="errorMessage" class="form-message form-message--error">
      {{ errorMessage }}
    </p>
    <p v-if="successMessage" class="form-message form-message--success">
      {{ successMessage }}
    </p>

    <div v-if="isLoading" class="history-grid" aria-live="polite">
      <article v-for="item in 2" :key="item" class="history-card history-card--loading">
        <span></span>
        <strong></strong>
        <p></p>
        <p></p>
      </article>
    </div>

    <div v-else-if="recipes.length" class="history-grid">
      <article
        v-for="recipe in recipes"
        :key="recipe.id"
        class="history-card history-card--openable"
        :data-blendy-from="`recipe-card-${recipe.id}`"
        role="button"
        tabindex="0"
        :aria-label="`Abrir detalle de ${recipe.nombre_plato}`"
        @click="openRecipe(recipe)"
        @keydown.enter.prevent="openRecipe(recipe)"
        @keydown.space.prevent="openRecipe(recipe)"
      >
        <header>
          <div>
            <span>{{ recipe.dificultad }} · {{ formatDate(recipe.fecha_creacion) }}</span>
            <h3>{{ recipe.nombre_plato }}</h3>
          </div>
          <strong>{{ recipe.tiempo_estimado }}</strong>
        </header>

        <section class="history-card__section">
          <h4>Ingredientes</h4>
          <ul>
            <li v-for="ingredient in recipe.ingredientes_json" :key="ingredient.nombre">
              {{ ingredient.cantidad }} de {{ ingredient.nombre }}
            </li>
          </ul>
        </section>

        <section class="history-card__section">
          <h4>Preparación</h4>
          <ol>
            <li v-for="step in recipe.pasos_json" :key="step">
              {{ step }}
            </li>
          </ol>
        </section>

        <footer @click.stop>
          <div class="rating-row" aria-label="Calificar receta">
            <button
              v-for="star in 5"
              :key="star"
              :disabled="busyRecipeId === recipe.id"
              type="button"
              @click.stop="submitRating(recipe, star)"
            >
              {{ star }}
            </button>
          </div>
          <button
            class="history-card__delete"
            :disabled="busyRecipeId === recipe.id"
            type="button"
            @click.stop="removeRecipe(recipe)"
          >
            Eliminar
          </button>
        </footer>
      </article>
    </div>

    <div v-else class="inventory-empty">
      <p class="workspace__label">Sin historial</p>
      <h3>Genera tu primera receta</h3>
      <p>Cuando el LLM responda, la receta quedará guardada en esta lista.</p>
    </div>
  </section>
</template>
