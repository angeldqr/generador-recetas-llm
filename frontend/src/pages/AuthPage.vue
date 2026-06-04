<script setup lang="ts">
import { useAuthSession } from '../composables/useAuthSession'
import { useStaggerReveal } from '../composables/useStaggerReveal'
import AuthPanel from '../components/AuthPanel.vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const { isAuthenticated, setToken } = useAuthSession()
const router = useRouter()
const pageRoot = ref<HTMLElement | null>(null)

if (isAuthenticated.value) {
  void router.replace('/inventario')
}

useStaggerReveal({
  root: pageRoot,
  selector: '.auth-card',
  delay: 0.15,
  stagger: 0.08,
  duration: 0.55,
})

function handleAuthenticated(token: string) {
  setToken(token)
  const redirect = router.currentRoute.value.query.redirect
  const target = typeof redirect === 'string' ? redirect : '/inventario'
  void router.replace(target)
}
</script>

<template>
  <article
    ref="pageRoot"
    class="page page--auth"
    data-route="auth"
  >
    <div class="auth-card" data-reveal>
      <p class="auth-card__eyebrow">Acceso</p>
      <h1 class="auth-card__title">Bienvenido de vuelta</h1>
      <p class="auth-card__hint">
        Inicia sesion para gestionar tu inventario y guardar recetas.
      </p>
      <AuthPanel @authenticated="handleAuthenticated" />
    </div>
  </article>
</template>

<style scoped>
.page--auth {
  width: min(720px, 100%);
  margin: 0 auto;
  padding-top: 56px;
}

.auth-card {
  display: grid;
  gap: 12px;
  padding: 36px;
  border: 1px solid rgb(15 36 24 / 0.08);
  border-radius: var(--radius-card);
  background:
    linear-gradient(160deg, rgb(254 253 248 / 0.96), rgb(244 241 232 / 0.92)),
    var(--color-panel);
  box-shadow: var(--shadow-card);
  transform-origin: top left;
}

.auth-card__eyebrow {
  margin: 0;
  color: var(--color-accent);
  font-family: "JetBrains Mono", monospace;
  font-size: 0.74rem;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.auth-card__title {
  margin: 0;
  font-family: "Bricolage Grotesque", system-ui;
  font-size: clamp(2.2rem, 5vw, 3.4rem);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.025em;
  color: var(--color-ink);
}

.auth-card__hint {
  margin: 0 0 12px;
  color: var(--color-muted);
  font-size: 0.98rem;
  line-height: 1.5;
}
</style>