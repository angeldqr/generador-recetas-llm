<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

const props = defineProps<{
  isAuthenticated: boolean
}>()

const emit = defineEmits<{
  logout: []
  'open-auth': [blendyId: string]
}>()

const router = useRouter()

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
      <template v-if="!isAuthenticated">
        <button
          class="nav__item"
          type="button"
          data-blendy-from="auth-nav"
          @click="emit('open-auth', 'auth-nav')"
        >
          <span>Iniciar sesion</span>
        </button>
      </template>
      <template v-else>
        <RouterLink
          :to="{ name: 'inventory' }"
          class="nav__item"
          active-class="nav__item--active"
        >
          Inventario
        </RouterLink>
        <RouterLink
          :to="{ name: 'recipes' }"
          class="nav__item"
          active-class="nav__item--active"
        >
          Recetas
        </RouterLink>
        <RouterLink
          :to="{ name: 'profile' }"
          class="nav__item"
          active-class="nav__item--active"
        >
          Perfil
        </RouterLink>
      </template>
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
      <button
        v-else
        class="header-action"
        type="button"
        data-blendy-from="auth-header"
        @click="emit('open-auth', 'auth-header')"
      >
        <span>Inicio</span>
      </button>
    </div>
  </header>
</template>
