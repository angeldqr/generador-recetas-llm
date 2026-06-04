<script setup lang="ts">
import { computed, ref } from 'vue'
import { generateRecipe } from '../services/api'
import type { Recipe } from '../types/api'
import BaseButton from './BaseButton.vue'

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
const successMessage = ref('')

const inventoryHint = computed(() => {
  if (props.ingredientCount === 0) return 'Agrega ingredientes antes de generar.'
  if (props.ingredientCount === 1) return '1 ingrediente en inventario.'
  return `${props.ingredientCount} ingredientes en inventario.`
})

async function handleGenerate() {
  if (props.ingredientCount <= 0 || isGenerating.value) {
    return
  }

  isGenerating.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const recipe = await generateRecipe(props.token)
    currentRecipe.value = recipe
    successMessage.value = 'Receta recibida. Revisala antes de guardarla como favorita.'
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
      <p class="workspace__label">Generacion</p>
      <h2 id="generator-title">Probar una receta</h2>
      <p>
        Usa el inventario actual como punto de partida y revisa la propuesta antes de repetirla o calificarla.
      </p>
    </div>

    <div class="recipe-generator__action">
      <BaseButton
        :disabled="ingredientCount === 0 || isGenerating"
        type="button"
        @click="handleGenerate"
      >
        {{ isGenerating ? 'Generando' : 'Generar receta' }}
      </BaseButton>
      <small>{{ inventoryHint }}</small>
    </div>

    <p v-if="errorMessage" class="form-message form-message--error">
      {{ errorMessage }}
    </p>
    <p v-if="successMessage" class="form-message form-message--success">
      {{ successMessage }}
    </p>

    <article v-if="isGenerating" class="recipe-card recipe-card--loading" aria-live="polite">
      <span></span>
      <strong></strong>
      <p></p>
      <p></p>
      <ul class="recipe-card__loading-steps" aria-label="Preparando respuesta">
        <li>Revisando inventario</li>
        <li>Armando pasos</li>
        <li>Estimando tiempo</li>
      </ul>
    </article>

    <article v-else-if="currentRecipe" class="recipe-card recipe-card--generated">
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
