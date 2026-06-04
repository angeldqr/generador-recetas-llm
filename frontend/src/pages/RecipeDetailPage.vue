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
  delay: 0.36,
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
    errorMessage.value = 'Necesitas iniciar sesion para ver esta receta.'
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
      :aria-label="`Volver a ${route.name === 'recipe-detail' ? 'recetas' : 'atras'}`"
      @click="goBack"
    >
      <span aria-hidden="true">&larr;</span>
      <span>Volver</span>
    </button>

    <div v-if="isLoading" class="recipe-detail__loading" aria-live="polite">
      <div class="recipe-detail__skeleton recipe-detail__skeleton--title"></div>
      <div class="recipe-detail__skeleton recipe-detail__skeleton--meta"></div>
      <div class="recipe-detail__skeleton recipe-detail__skeleton--body"></div>
    </div>

    <p v-else-if="errorMessage" class="recipe-detail__error">{{ errorMessage }}</p>

    <p v-else-if="!currentRecipe" class="recipe-detail__error">
      La receta solicitada no existe o ya no esta disponible.
    </p>

    <article
      v-else
      class="recipe-detail"
    >
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
  border: 1px solid rgb(15 36 24 / 0.08);
  border-radius: 32px;
  padding: 36px;
  background:
    linear-gradient(160deg, rgb(254 253 248 / 0.96), rgb(244 241 232 / 0.92)),
    var(--color-panel);
  box-shadow: var(--shadow-card);
  transform-origin: top center;
}

.recipe-detail__header {
  display: grid;
  gap: 14px;
  margin-bottom: 28px;
}

.recipe-detail__eyebrow {
  margin: 0;
  color: var(--color-accent);
  font-family: "JetBrains Mono", monospace;
  font-size: 0.74rem;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.recipe-detail__title {
  margin: 0;
  font-family: "Bricolage Grotesque", system-ui;
  font-size: clamp(2.6rem, 6vw, 4.6rem);
  font-weight: 700;
  line-height: 0.92;
  letter-spacing: -0.03em;
  color: var(--color-ink);
}

.recipe-detail__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.recipe-detail__chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: var(--radius-button);
  padding: 7px 14px;
  color: var(--color-accent-strong);
  background: var(--color-accent-soft);
  font-family: "DM Sans", system-ui;
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: -0.005em;
}

.recipe-detail__grid {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 28px;
  border-top: 1px solid var(--color-line);
  padding-top: 28px;
}

.recipe-detail__section h2 {
  margin: 0 0 12px;
  font-family: "Bricolage Grotesque", system-ui;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--color-ink);
}

.recipe-detail__section ul,
.recipe-detail__section ol {
  display: grid;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
  color: var(--color-ink-soft);
  line-height: 1.55;
  font-size: 0.96rem;
}

.recipe-detail__section ul li {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 10px 14px;
  border: 1px solid rgb(15 36 24 / 0.06);
  border-radius: 14px;
  background: var(--color-soft);
}

.recipe-detail__section ol li {
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 12px;
  align-items: start;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-line);
}

.recipe-detail__section ol li:last-child {
  border-bottom: 0;
}

.recipe-detail__section ol li::before {
  content: counter(list-item);
  display: grid;
  place-items: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-ink);
  color: var(--color-panel);
  font-family: "Bricolage Grotesque", system-ui;
  font-size: 0.82rem;
  font-weight: 700;
  flex-shrink: 0;
}

.recipe-detail__section ol {
  counter-reset: list-item;
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
