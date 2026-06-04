<script setup lang="ts">
import AppHeader from './AppHeader.vue'

defineProps<{
  isAuthenticated: boolean
}>()

const emit = defineEmits<{
  logout: []
}>()
</script>

<template>
  <div class="app-shell">
    <AppHeader
      :is-authenticated="isAuthenticated"
      @logout="emit('logout')"
    />
    <slot />
  </div>
</template>
