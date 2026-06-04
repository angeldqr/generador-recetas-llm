<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getRecipes } from '../services/api'
import { useStaggerReveal } from '../composables/useStaggerReveal'
import type { Recipe } from '../types/api'

const props = defineProps<{
  id: string
}>()

const route = useRoute()
const router = useRouter()
const recipes = ref<Recipe[]>([])
const isLoading = ref(true)
const errorMessage = ref('')
const pageRoot = ref<HTMLElement | null>(null)

useStaggerReveal({
  root: pageRoot,
  selector: '.recipe-detail__header, .recipe-detail__section',
  delay: 0.32,
  stagger: 0.08,
  duration: 0.55,
})

const currentRecipe = computed<Recipe | null>(() => {
  const id = Number(props.id)
  if (!Number.isFinite(id)) return null
  return recipes.value.find((recipe) => recipe.id === id) ?? null
})

function formatDate(value: string) {
  return new Intl.DateTimeFormat('es-CO', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(new Date(value))
}

onMounted(async () => {
  const token = localStorage.getItem('recetas_llm_token') ?? ''
  if (!token) {
    isLoading.value = false
    errorMessage.value = 'Necesitas iniciar sesión para ver esta receta.'
    return
  }

  try {
    recipes.value = await getRecipes(token)
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo cargar la receta.'
  } finally {
    isLoading.value = false
  }
})

function goBack() {
  if (window.history.length > 1) {
    router.back()
  } else {
    void router.push({ name: 'recipes' })
  }
}
</script>

<template>
  <article ref="pageRoot" class="page page--recipe-detail" data-route="recipe-detail">
    <button
      class="recipe-detail__back"
      type="button"
      :aria-label="`Volver a ${route.name === 'recipe-detail' ? 'recetas' : 'atrás'}`"
      @click="goBack"
    >
      <span aria-hidden="true">←</span>
      <span>Volver</span>
    </button>

    <div v-if="isLoading" class="recipe-detail__loading" aria-live="polite">
      <div class="recipe-detail__skeleton recipe-detail__skeleton--title"></div>
      <div class="recipe-detail__skeleton recipe-detail__skeleton--meta"></div>
      <div class="recipe-detail__skeleton recipe-detail__skeleton--body"></div>
    </div>

    <p v-else-if="errorMessage" class="recipe-detail__error">{{ errorMessage }}</p>

    <p v-else-if="!currentRecipe" class="recipe-detail__error">
      La receta solicitada no existe o ya no está disponible.
    </p>

    <article v-else class="recipe-detail" data-blendy-to="recipe-detail">
      <header class="recipe-detail__header">
        <p class="recipe-detail__eyebrow">Receta guardada</p>
        <h1 class="recipe-detail__title">{{ currentRecipe.nombre_plato }}</h1>
        <div class="recipe-detail__meta">
          <span class="recipe-detail__chip">{{ currentRecipe.dificultad }}</span>
          <span class="recipe-detail__chip">{{ currentRecipe.tiempo_estimado }}</span>
          <span class="recipe-detail__chip">{{ formatDate(currentRecipe.fecha_creacion) }}</span>
        </div>
      </header>

      <div class="recipe-detail__grid">
        <section class="recipe-detail__section">
          <h2>Ingredientes</h2>
          <ul>
            <li
              v-for="ingredient in currentRecipe.ingredientes_json"
              :key="ingredient.nombre"
            >
              {{ ingredient.cantidad }} de {{ ingredient.nombre }}
            </li>
          </ul>
        </section>

        <section class="recipe-detail__section">
          <h2>Pasos</h2>
          <ol>
            <li v-for="(step, index) in currentRecipe.pasos_json" :key="index">
              {{ step }}
            </li>
          </ol>
        </section>
      </div>
    </article>
  </article>
</template>

<style scoped>
.page--recipe-detail {
  width: min(880px, 100%);
  margin: 0 auto;
  padding-top: 12px;
}

.recipe-detail__back {
  display: inline-flex;
  gap: 10px;
  align-items: center;
  min-height: 40px;
  border: 1px solid var(--color-line);
  border-radius: var(--radius-button);
  padding: 0 16px;
  color: var(--color-ink);
  background: #ffffff;
  font-weight: 800;
  transition:
    transform 150ms var(--ease-out),
    border-color 180ms ease,
    color 180ms ease;
}

.recipe-detail__back:active {
  transform: scale(0.97);
}

@media (hover: hover) and (pointer: fine) {
  .recipe-detail__back:hover {
    border-color: rgb(38 116 81 / 0.28);
    color: var(--color-accent-strong);
  }
}

.recipe-detail {
  margin-top: 20px;
  border: 1px solid var(--color-line);
  border-radius: 28px;
  padding: 32px;
  background:
    linear-gradient(160deg, rgb(255 255 255 / 0.96), rgb(246 247 242 / 0.94)),
    #ffffff;
  box-shadow: var(--shadow-soft);
  transform-origin: top center;
}

.recipe-detail__header {
  display: grid;
  gap: 12px;
  margin-bottom: 24px;
}

.recipe-detail__eyebrow {
  margin: 0;
  color: var(--color-accent);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.recipe-detail__title {
  margin: 0;
  font-size: clamp(2.4rem, 6vw, 4.6rem);
  line-height: 0.95;
}

.recipe-detail__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.recipe-detail__chip {
  border-radius: var(--radius-button);
  padding: 6px 12px;
  color: var(--color-accent-strong);
  background: rgb(38 116 81 / 0.1);
  font-size: 0.82rem;
  font-weight: 850;
}

.recipe-detail__grid {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 24px;
  border-top: 1px solid var(--color-line);
  padding-top: 24px;
}

.recipe-detail__section h2 {
  margin: 0 0 10px;
  font-size: 1.05rem;
  letter-spacing: 0;
}

.recipe-detail__section ul,
.recipe-detail__section ol {
  display: grid;
  gap: 10px;
  margin: 0;
  padding-left: 22px;
  color: var(--color-muted);
  line-height: 1.6;
}

.recipe-detail__loading {
  margin-top: 20px;
  display: grid;
  gap: 14px;
}

.recipe-detail__skeleton {
  border-radius: var(--radius-card);
  background: linear-gradient(90deg, #edf2eb, #f8faf5, #edf2eb);
  background-size: 200% 100%;
  animation: skeleton-shift 1.2s linear infinite;
}

.recipe-detail__skeleton--title {
  min-height: 64px;
}

.recipe-detail__skeleton--meta {
  min-height: 32px;
  width: 60%;
}

.recipe-detail__skeleton--body {
  min-height: 220px;
}

.recipe-detail__error {
  margin-top: 24px;
  border-radius: 18px;
  padding: 16px;
  color: var(--color-danger);
  background: rgb(163 61 61 / 0.1);
  font-weight: 700;
}

@keyframes skeleton-shift {
  to {
    background-position: -200% 0;
  }
}

@media (max-width: 820px) {
  .recipe-detail {
    padding: 22px;
  }

  .recipe-detail__grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
