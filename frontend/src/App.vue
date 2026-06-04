<template>
  <main class="starter">
    <section>
      <p class="starter__eyebrow">Recetas LLM</p>
      <h1>Frontend Vue listo para construir</h1>
      <p>
        Esta base conectará el inventario, la generación de recetas y el
        historial con la API de FastAPI.
      </p>
    </section>
  </main>
</template>

<style scoped>
.starter {
  min-height: 100dvh;
  display: grid;
  place-items: center;
  padding: 48px 20px;
  color: var(--color-ink);
  background: var(--color-soft);
}

.starter section {
  width: min(640px, 100%);
}

.starter__eyebrow {
  margin: 0 0 12px;
  color: var(--color-accent);
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.starter h1 {
  margin: 0;
  font-size: clamp(2.4rem, 7vw, 5rem);
  line-height: 0.95;
  letter-spacing: 0;
}

.starter p {
  max-width: 54ch;
  color: var(--color-muted);
  font-size: 1.05rem;
  line-height: 1.7;
}
</style>
