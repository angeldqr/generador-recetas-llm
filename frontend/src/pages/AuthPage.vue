<script setup lang="ts">
import { useRouter } from 'vue-router'
import AuthPanel from '../components/AuthPanel.vue'

const emit = defineEmits<{
  authenticated: [token: string]
}>()

const router = useRouter()

function handleAuthenticated(token: string) {
  emit('authenticated', token)
  const redirect = router.currentRoute.value.query.redirect
  const target = typeof redirect === 'string' ? redirect : '/inventario'
  void router.replace(target)
}
</script>

<template>
  <article class="page page--auth" data-route="auth">
    <AuthPanel @authenticated="handleAuthenticated" />
  </article>
</template>

<style scoped>
.page--auth {
  width: min(1180px, 100%);
  margin: 0 auto;
  padding-top: 24px;
}
</style>
