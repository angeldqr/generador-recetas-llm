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
      <button class="cta cta--primary" type="button" @click="goHome">
        <span class="cta__label">Ir al inicio</span>
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
  font-family: "JetBrains Mono", monospace;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.2em;
}

.not-found__title {
  margin: 12px 0 18px;
  font-family: "Bricolage Grotesque", system-ui;
  font-size: clamp(2.6rem, 6vw, 4.4rem);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.03em;
  color: var(--color-ink);
}

.not-found__body {
  margin: 0 auto 28px;
  max-width: 44ch;
  color: var(--color-muted);
  font-family: "DM Sans", system-ui;
  line-height: 1.6;
}

.cta {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  min-height: 54px;
  padding: 0 28px;
  border: 0;
  border-radius: var(--radius-button);
  font-family: "DM Sans", system-ui;
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: -0.01em;
  cursor: pointer;
  transition:
    transform 200ms var(--ease-out),
    box-shadow 200ms ease;
}

.cta--primary {
  color: var(--color-panel);
  background:
    linear-gradient(180deg, #3a8a64, var(--color-accent) 78%),
    var(--color-accent);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.18),
    0 18px 40px -12px rgb(38 116 81 / 0.55);
}

.cta--primary:active {
  transform: scale(0.97);
}
</style>
