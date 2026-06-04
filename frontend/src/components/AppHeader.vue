<script setup lang="ts">
defineProps<{
  activeView: string
  isAuthenticated: boolean
}>()

const emit = defineEmits<{
  navigate: [view: string]
  logout: []
}>()

const publicItems = [
  { id: 'auth', label: 'Acceso' },
  { id: 'preview', label: 'Vista previa' },
]

const privateItems = [
  { id: 'inventory', label: 'Inventario' },
  { id: 'recipes', label: 'Recetas' },
]
</script>

<template>
  <header class="app-header">
    <button class="brand" type="button" @click="emit('navigate', isAuthenticated ? 'inventory' : 'auth')">
      <span class="brand__mark" aria-hidden="true">R</span>
      <span>
        <strong>Recetas LLM</strong>
        <small>Inventario inteligente</small>
      </span>
    </button>

    <nav class="nav" aria-label="Principal">
      <button
        v-for="item in isAuthenticated ? privateItems : publicItems"
        :key="item.id"
        class="nav__item"
        :class="{ 'nav__item--active': activeView === item.id }"
        type="button"
        @click="emit('navigate', item.id)"
      >
        {{ item.label }}
      </button>
    </nav>

    <button
      v-if="isAuthenticated"
      class="header-action header-action--ghost"
      type="button"
      @click="emit('logout')"
    >
      Cerrar sesión
    </button>
    <button
      v-else
      class="header-action"
      type="button"
      @click="emit('navigate', 'auth')"
    >
      Entrar
    </button>
  </header>
</template>
