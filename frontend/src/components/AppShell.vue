<script setup lang="ts">
import AppHeader from './AppHeader.vue'

defineProps<{
  isAuthenticated: boolean
}>()

const emit = defineEmits<{
  logout: []
  'open-auth': [blendyId: string]
}>()
</script>

<template>
  <div class="app-shell">
    <AppHeader
      :is-authenticated="isAuthenticated"
      @logout="emit('logout')"
      @open-auth="(id: string) => emit('open-auth', id)"
    />
    <slot />
  </div>
</template>
