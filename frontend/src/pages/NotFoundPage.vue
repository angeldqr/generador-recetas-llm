<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  void router.push({ name: 'welcome' })
}
</script>

<template>
  <article class="page page--not-found" data-route="not-found">
    <section class="not-found">
      <p class="not-found__eyebrow">404</p>
      <h1 class="not-found__title">No encontramos esa ruta</h1>
      <p class="not-found__body">
        La pagina que buscas no existe o se movio. Vuelve al inicio para continuar.
      </p>
      <button class="pill-button" type="button" @click="goHome">
        Ir al inicio
      </button>
    </section>
  </article>
</template>

<style scoped>
.page--not-found {
  width: min(640px, 100%);
  margin: 0 auto;
  padding-top: 80px;
  text-align: center;
}

.not-found__eyebrow {
  margin: 0;
  color: var(--color-accent);
  font-size: 0.9rem;
  font-weight: 800;
  letter-spacing: 0.18em;
}

.not-found__title {
  margin: 12px 0 18px;
  font-size: clamp(2.4rem, 6vw, 4.6rem);
  line-height: 0.95;
}

.not-found__body {
  margin: 0 auto 24px;
  max-width: 44ch;
  color: var(--color-muted);
  line-height: 1.6;
}
</style>
