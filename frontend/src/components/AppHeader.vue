<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

const props = defineProps<{
  isAuthenticated: boolean
}>()

const emit = defineEmits<{
  logout: []
}>()

const router = useRouter()

type NavItem = {
  id: string
  label: string
  to: { name: string }
}

const publicItems: NavItem[] = [
  { id: 'auth', label: 'Iniciar sesion', to: { name: 'auth' } },
]

const privateItems: NavItem[] = [
  { id: 'inventory', label: 'Inventario', to: { name: 'inventory' } },
  { id: 'recipes', label: 'Recetas', to: { name: 'recipes' } },
  { id: 'profile', label: 'Perfil', to: { name: 'profile' } },
]

const items = computed(() =>
  props.isAuthenticated ? privateItems : publicItems,
)

const brandTarget = computed(() =>
  props.isAuthenticated ? { name: 'inventory' } : { name: 'welcome' },
)

async function navigateToBrand() {
  await router.push(brandTarget.value)
}
</script>

<template>
  <header class="app-header">
    <button
      class="brand"
      type="button"
      aria-label="Ir al inicio"
      @click="navigateToBrand"
    >
      <span class="brand__mark" aria-hidden="true">R</span>
      <span>
        <strong>Recetas LLM</strong>
        <small>Inventario inteligente</small>
      </span>
    </button>

    <nav class="nav" aria-label="Principal">
      <RouterLink
        v-for="item in items"
        :key="item.id"
        :to="item.to"
        class="nav__item"
        active-class="nav__item--active"
      >
        {{ item.label }}
      </RouterLink>
    </nav>

    <div class="header-actions">
      <button
        v-if="isAuthenticated"
        class="header-action header-action--ghost"
        type="button"
        @click="emit('logout')"
      >
        Cerrar sesion
      </button>
      <RouterLink
        v-else
        :to="{ name: 'welcome' }"
        class="header-action"
      >
        Inicio
      </RouterLink>
    </div>
  </header>
</template>
