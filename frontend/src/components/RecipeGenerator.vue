<script setup lang="ts">
import { ref } from 'vue'
import { generateRecipe } from '../services/api'
import type { Recipe } from '../types/api'

const props = defineProps<{
  token: string
  ingredientCount: number
}>()

const emit = defineEmits<{
  generated: [recipe: Recipe]
}>()

const currentRecipe = ref<Recipe | null>(null)
const isGenerating = ref(false)
const errorMessage = ref('')

async function handleGenerate() {
  if (props.ingredientCount <= 0 || isGenerating.value) {
    return
  }

  isGenerating.value = true
  errorMessage.value = ''

  try {
    const recipe = await generateRecipe(props.token)
    currentRecipe.value = recipe
    emit('generated', recipe)
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo generar la receta.'
  } finally {
    isGenerating.value = false
  }
}
</script>

<template>
  <section class="recipe-generator" aria-labelledby="generator-title">
    <div class="recipe-generator__copy">
      <p class="workspace__label">Generación</p>
      <h2 id="generator-title">Receta desde tu inventario</h2>
      <p>
        El LLM recibe tus ingredientes actuales y devuelve una receta guardada
        con ingredientes, pasos, tiempo y dificultad.
      </p>
    </div>

    <div class="recipe-generator__action">
      <button
        class="pill-button"
        :disabled="ingredientCount === 0 || isGenerating"
        type="button"
        @click="handleGenerate"
      >
        {{ isGenerating ? 'Generando receta' : 'Generar receta' }}
      </button>
      <small v-if="ingredientCount === 0">
        Agrega ingredientes antes de generar.
      </small>
      <small v-else>
        {{ ingredientCount }} ingredientes listos.
      </small>
    </div>

    <p v-if="errorMessage" class="form-message form-message--error">
      {{ errorMessage }}
    </p>

    <article v-if="isGenerating" class="recipe-card recipe-card--loading" aria-live="polite">
      <span></span>
      <strong></strong>
      <p></p>
      <p></p>
    </article>

    <article v-else-if="currentRecipe" class="recipe-card">
      <div class="recipe-card__header">
        <div>
          <span>{{ currentRecipe.dificultad }}</span>
          <h3>{{ currentRecipe.nombre_plato }}</h3>
        </div>
        <strong>{{ currentRecipe.tiempo_estimado }}</strong>
      </div>

      <div class="recipe-card__grid">
        <section>
          <h4>Ingredientes</h4>
          <ul>
            <li v-for="ingredient in currentRecipe.ingredientes_json" :key="ingredient.nombre">
              {{ ingredient.cantidad }} de {{ ingredient.nombre }}
            </li>
          </ul>
        </section>

        <section>
          <h4>Pasos</h4>
          <ol>
            <li v-for="step in currentRecipe.pasos_json" :key="step">
              {{ step }}
            </li>
          </ol>
        </section>
      </div>
    </article>
  </section>
</template>
