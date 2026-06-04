<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {
  createIngredient,
  deleteIngredient,
  getIngredients,
  updateIngredient,
} from '../services/api'
import type { Ingredient } from '../types/api'

const props = defineProps<{
  token: string
}>()

const emit = defineEmits<{
  updated: [ingredients: Ingredient[]]
}>()

const ingredients = ref<Ingredient[]>([])
const name = ref('')
const quantity = ref('')
const unit = ref('unidad')
const editingId = ref<number | null>(null)
const isLoading = ref(false)
const isSaving = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

function resetForm() {
  name.value = ''
  quantity.value = ''
  unit.value = 'unidad'
  editingId.value = null
}

function publishIngredients(nextIngredients: Ingredient[]) {
  ingredients.value = nextIngredients
  emit('updated', nextIngredients)
}

async function loadIngredients() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    publishIngredients(await getIngredients(props.token))
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo cargar el inventario.'
  } finally {
    isLoading.value = false
  }
}

function validateForm() {
  const parsedQuantity = Number(quantity.value)

  if (name.value.trim().length < 2) {
    return 'El ingrediente debe tener al menos 2 caracteres.'
  }

  if (!Number.isFinite(parsedQuantity) || parsedQuantity <= 0) {
    return 'La cantidad debe ser mayor que cero.'
  }

  if (unit.value.trim().length < 1) {
    return 'Indica una unidad.'
  }

  return ''
}

async function submitIngredient() {
  const validationError = validateForm()

  if (validationError) {
    errorMessage.value = validationError
    return
  }

  isSaving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  const payload = {
    nombre: name.value.trim(),
    cantidad: Number(quantity.value),
    unidad: unit.value.trim(),
  }

  try {
    if (editingId.value) {
      await updateIngredient(editingId.value, payload, props.token)
      successMessage.value = 'Ingrediente actualizado.'
    } else {
      await createIngredient(payload, props.token)
      successMessage.value = 'Ingrediente agregado.'
    }

    resetForm()
    await loadIngredients()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo guardar el ingrediente.'
  } finally {
    isSaving.value = false
  }
}

function startEdit(ingredient: Ingredient) {
  editingId.value = ingredient.id
  name.value = ingredient.nombre
  quantity.value = String(ingredient.cantidad)
  unit.value = ingredient.unidad
  successMessage.value = ''
  errorMessage.value = ''
}

async function removeIngredient(ingredient: Ingredient) {
  isSaving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await deleteIngredient(ingredient.id, props.token)
    successMessage.value = `${ingredient.nombre} eliminado.`
    await loadIngredients()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo eliminar el ingrediente.'
  } finally {
    isSaving.value = false
  }
}

onMounted(loadIngredients)
</script>

<template>
  <section class="inventory-panel" aria-labelledby="inventory-title">
    <div class="inventory-panel__header">
      <div>
        <p class="workspace__label">Inventario</p>
        <h2 id="inventory-title">Ingredientes disponibles</h2>
      </div>
      <span class="inventory-count">{{ ingredients.length }} registrados</span>
    </div>

    <form class="ingredient-form" @submit.prevent="submitIngredient">
      <label>
        <span>Ingrediente</span>
        <input v-model="name" placeholder="Arroz" />
      </label>
      <label>
        <span>Cantidad</span>
        <input v-model="quantity" inputmode="decimal" placeholder="2" type="number" />
      </label>
      <label>
        <span>Unidad</span>
        <input v-model="unit" placeholder="tazas" />
      </label>
      <button class="pill-button ingredient-form__button" :disabled="isSaving" type="submit">
        {{ editingId ? 'Guardar cambios' : 'Agregar' }}
      </button>
      <button
        v-if="editingId"
        class="pill-button pill-button--light ingredient-form__button"
        type="button"
        @click="resetForm"
      >
        Cancelar
      </button>
    </form>

    <p v-if="errorMessage" class="form-message form-message--error">
      {{ errorMessage }}
    </p>
    <p v-if="successMessage" class="form-message form-message--success">
      {{ successMessage }}
    </p>

    <div v-if="isLoading" class="inventory-grid" aria-live="polite">
      <article v-for="item in 3" :key="item" class="ingredient-card ingredient-card--skeleton">
        <span></span>
        <strong></strong>
        <div></div>
      </article>
    </div>

    <div v-else-if="ingredients.length" class="inventory-grid">
      <article v-for="ingredient in ingredients" :key="ingredient.id" class="ingredient-card">
        <span>{{ ingredient.unidad }}</span>
        <strong>{{ ingredient.cantidad }} {{ ingredient.nombre }}</strong>
        <div class="ingredient-card__actions">
          <button type="button" @click="startEdit(ingredient)">Editar</button>
          <button type="button" @click="removeIngredient(ingredient)">Eliminar</button>
        </div>
      </article>
    </div>

    <div v-else class="inventory-empty">
      <p class="workspace__label">Sin ingredientes</p>
      <h3>Agrega lo que tengas en casa</h3>
      <p>
        Con dos o tres ingredientes ya puedes probar la generación de recetas.
      </p>
    </div>
  </section>
</template>
