<script setup lang="ts">
import { useAuthSession } from '../composables/useAuthSession'
import AuthPanel from '../components/AuthPanel.vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const { isAuthenticated, setToken } = useAuthSession()
const router = useRouter()
const isReady = ref(false)

if (isAuthenticated.value) {
  void router.replace('/inventario')
} else {
  isReady.value = true
}

function handleAuthenticated(token: string) {
  setToken(token)
  const redirect = router.currentRoute.value.query.redirect
  const target = typeof redirect === 'string' ? redirect : '/inventario'
  void router.replace(target)
}
</script>

<template>
  <article v-if="isReady" class="page page--auth" data-route="auth">
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
