<script setup lang="ts">
import AppHeader from './AppHeader.vue'

defineProps<{
  activeView: string
  isAuthenticated: boolean
}>()

const emit = defineEmits<{
  navigate: [view: string]
  logout: []
}>()
</script>

<template>
  <div class="app-shell">
    <AppHeader
      :active-view="activeView"
      :is-authenticated="isAuthenticated"
      @navigate="emit('navigate', $event)"
      @logout="emit('logout')"
    />
    <slot />
  </div>
</template>
