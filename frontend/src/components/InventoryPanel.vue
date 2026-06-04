<script setup lang="ts">
import { computed, nextTick, onMounted, ref } from 'vue'
import gsap from 'gsap'
import {
  createIngredient,
  deleteIngredient,
  getIngredients,
  updateIngredient,
} from '../services/api'
import type { Ingredient } from '../types/api'
import BaseButton from './BaseButton.vue'
import BaseInput from './BaseInput.vue'

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
const nameInput = ref<InstanceType<typeof BaseInput> | null>(null)
const gridRef = ref<HTMLElement | null>(null)

const PREDEFINED_UNITS = [
  'unidad',
  'gramos',
  'kilogramos',
  'tazas',
  'cucharadas',
  'cucharaditas',
  'ml',
  'litros',
  'libras',
  'onzas',
  'pizca',
  'hojas',
  'dientes',
  'rodajas',
  'trozos',
  'paquetes',
]

const COMMON_SUGGESTIONS = [
  'Arroz', 'Pollo', 'Carne molida', 'Cebolla', 'Ajo', 'Tomate', 'Papa', 'Zanahoria',
  'Huevo', 'Leche', 'Queso', 'Pan', 'Pasta', 'Aceite', 'Sal', 'Pimienta',
  'Frijoles', 'Lentejas', 'Pollo', 'Pescado', 'Camarón', 'Lechuga', 'Aguacate',
  'Limón', 'Cilantro', 'Pimentón', 'Chile', 'Mantequilla', 'Azúcar', 'Harina',
  'Yogurt', 'Naranja', 'Plátano', 'Manzana', 'Espinaca', 'Brócoli', 'Calabacín',
  'Champiñón', 'Jamón', 'Tocino', 'Salchicha', 'Maíz', 'Chícharo', 'Espinaca',
  'Crema', 'Salsa de tomate', 'Mostaza', 'Mayonesa', 'Soya', 'Vinagre',
]

const countLabel = computed(() => {
  const count = ingredients.value.length
  return count === 1 ? '1 ingrediente' : `${count} ingredientes`
})

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
    await nextTick()
    animateGridIn()
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo cargar el inventario.'
  } finally {
    isLoading.value = false
  }
}

function animateGridIn() {
  if (!gridRef.value) return
  const cards = gridRef.value.querySelectorAll<HTMLElement>('.ingredient-card')
  if (!cards.length) return
  gsap.fromTo(
    cards,
    { autoAlpha: 0, y: 20, scale: 0.96 },
    {
      autoAlpha: 1,
      y: 0,
      scale: 1,
      duration: 0.35,
      ease: 'power2.out',
      stagger: 0.05,
    }
  )
}

function animateCardOut(card: HTMLElement, onComplete: () => void) {
  gsap.to(card, {
    autoAlpha: 0,
    scale: 0.94,
    y: -10,
    duration: 0.22,
    ease: 'power2.in',
    onComplete,
  })
}

function validateForm() {
  const parsedQuantity = Number(quantity.value)

  if (name.value.trim().length < 2) {
    return 'El ingrediente debe tener al menos 2 caracteres.'
  }

  if (!Number.isFinite(parsedQuantity) || parsedQuantity <= 0) {
    return 'La cantidad debe ser mayor que cero.'
  }

  if (!unit.value || unit.value.trim().length < 1) {
    return 'Selecciona una unidad.'
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
    nombre: name.value.trim().toLowerCase(),
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
  nameInput.value?.focus()
}

async function removeIngredient(ingredient: Ingredient, event: Event) {
  const card = (event.target as HTMLElement).closest('.ingredient-card') as HTMLElement
  if (!card) return

  isSaving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await deleteIngredient(ingredient.id, props.token)
    successMessage.value = `${ingredient.nombre} eliminado.`
    animateCardOut(card, async () => {
      await loadIngredients()
      isSaving.value = false
    })
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'No se pudo eliminar el ingrediente.'
    isSaving.value = false
  }
}

function focusFirstField() {
  nameInput.value?.focus()
}

function getIngredientIcon(name: string): string {
  const icons: Record<string, string> = {
    arroz: '🍚', pollo: '🍗', carne: '🥩', pescado: '🐟', camarón: '🦐',
    huevo: '🥚', leche: '🥛', queso: '🧀', pan: '🍞', pasta: '🍝',
    cebolla: '🧅', ajo: '🧄', tomate: '🍅', papa: '🥔', zanahoria: '🥕',
    lechuga: '🥬', espinaca: '🍃', brócoli: '🥦', calabacín: '🥒', champiñón: '🍄',
    aguacate: '🥑', limón: '🍋', naranja: '🍊', plátano: '🍌', manzana: '🍎',
    maíz: '🌽', frijoles: '🫘', lentejas: '🫘', soya: '🫘',
    mantequilla: '🧈', aceite: '🫒', sal: '🧂', azúcar: '🍬', harina: '🌾',
    jamón: '🥓', tocino: '🥓', salchicha: '🌭', yogurt: '🥣',
    crema: '🥛', salsa: '🥫', mostaza: '🌭', mayonesa: '🥪', vinagre: '🍶',
    cilantro: '🌿', pimentón: '🌶️', chile: '🌶️', pimiento: '🫑',
    hoja: '🍃', diente: '🧄', rodaja: '🍋', trozo: '🧊',
  }
  const key = Object.keys(icons).find(k => name.toLowerCase().includes(k))
  return key ? icons[key] : '🥘'
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
      <span class="inventory-count">{{ countLabel }}</span>
    </div>

    <form class="ingredient-form" @submit.prevent="submitIngredient">
      <div class="form-group form-group--name">
        <BaseInput
          ref="nameInput"
          v-model="name"
          label="Ingrediente"
          placeholder="Ej: Arroz, Pollo, Huevo..."
          autocomplete="off"
          list="ingredient-suggestions"
        />
        <datalist id="ingredient-suggestions">
          <option v-for="suggestion in COMMON_SUGGESTIONS" :key="suggestion" :value="suggestion" />
        </datalist>
      </div>

      <div class="form-group form-group--quantity">
        <label class="form-label">
          <span>Cantidad</span>
          <input
            v-model="quantity"
            inputmode="decimal"
            placeholder="2"
            type="number"
            min="0.1"
            step="0.1"
          />
        </label>
      </div>

      <div class="form-group form-group--unit">
        <label class="form-label">
          <span>Unidad</span>
          <select v-model="unit">
            <option v-for="u in PREDEFINED_UNITS" :key="u" :value="u">
              {{ u }}
            </option>
          </select>
        </label>
      </div>

      <BaseButton class="ingredient-form__button" :disabled="isSaving" type="submit">
        {{ editingId ? 'Guardar' : 'Agregar' }}
      </BaseButton>
      <BaseButton
        v-if="editingId"
        class="ingredient-form__button"
        variant="soft"
        type="button"
        @click="resetForm"
      >
        Cancelar
      </BaseButton>
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

    <div v-else-if="ingredients.length" ref="gridRef" class="inventory-grid">
      <article
        v-for="ingredient in ingredients"
        :key="ingredient.id"
        class="ingredient-card"
      >
        <div class="ingredient-card__icon">
          {{ getIngredientIcon(ingredient.nombre) }}
        </div>
        <div class="ingredient-card__body">
          <strong>{{ ingredient.nombre }}</strong>
          <span class="ingredient-card__meta">
            {{ ingredient.cantidad }} {{ ingredient.unidad }}
          </span>
        </div>
        <div class="ingredient-card__actions">
          <button type="button" @click="startEdit(ingredient)">Editar</button>
          <button type="button" @click="removeIngredient(ingredient, $event)">Eliminar</button>
        </div>
      </article>
    </div>

    <div v-else class="inventory-empty">
      <div class="inventory-empty__mark" aria-hidden="true">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <p class="workspace__label">Sin ingredientes</p>
      <h3>Empieza por lo que tienes</h3>
      <p>
        Agrega los ingredientes que tienes en casa. El generador de recetas se activa cuando tu inventario tiene al menos un ingrediente.
      </p>
      <BaseButton type="button" variant="soft" @click="focusFirstField">
        Agregar primer ingrediente
      </BaseButton>
    </div>
  </section>
</template>

<style>
@import '../styles/inventory.css';

.form-group {
  display: grid;
  gap: 8px;
}

.form-group--name {
  grid-column: 1 / -1;
}

.form-label {
  display: grid;
  gap: 8px;
  color: var(--color-ink);
  font-family: "DM Sans", system-ui;
  font-weight: 600;
  font-size: 0.88rem;
  letter-spacing: -0.005em;
}

.form-label input,
.form-label select {
  min-height: 50px;
  width: 100%;
  border: 1px solid rgb(15 36 24 / 0.1);
  border-radius: 16px;
  padding: 0 16px;
  color: var(--color-ink);
  background: var(--color-soft);
  font-family: "DM Sans", system-ui;
  font-size: 0.96rem;
  outline: none;
  transition:
    border-color 180ms ease,
    box-shadow 180ms ease,
    background 180ms ease;
  appearance: none;
  cursor: pointer;
}

.form-label select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
}

.form-label input:focus,
.form-label select:focus {
  border-color: var(--color-accent);
  background: var(--color-panel);
  box-shadow: 0 0 0 4px rgb(38 116 81 / 0.16);
}

.form-label input::placeholder {
  color: var(--color-muted);
  font-weight: 500;
}

.ingredient-card__icon {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: var(--color-accent-soft);
  font-size: 1.6rem;
  line-height: 1;
}

.ingredient-card__body {
  display: grid;
  gap: 4px;
}

.ingredient-card__meta {
  color: var(--color-muted);
  font-family: "JetBrains Mono", monospace;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.ingredient-card strong {
  font-size: clamp(1.2rem, 2.2vw, 1.6rem);
}

@media (max-width: 980px) {
  .ingredient-form {
    grid-template-columns: 1fr 1fr;
  }
  .form-group--name {
    grid-column: 1 / -1;
  }
}

@media (max-width: 560px) {
  .ingredient-form {
    grid-template-columns: 1fr;
  }
  .form-group--name {
    grid-column: auto;
  }
}
</style>
