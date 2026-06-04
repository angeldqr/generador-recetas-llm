<script setup lang="ts">
import { useAuthSession } from '../composables/useAuthSession'
import { useBlendyOnMount } from '../composables/useBlendy'
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
  useBlendyOnMount({ id: 'auth-cta' })
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
    <div class="auth-entry" data-blendy-to="auth-cta">
      <AuthPanel @authenticated="handleAuthenticated" />
    </div>
  </article>
</template>

<style scoped>
.page--auth {
  width: min(1180px, 100%);
  margin: 0 auto;
  padding-top: 24px;
}

.auth-entry {
  transform-origin: top left;
}
</style>
