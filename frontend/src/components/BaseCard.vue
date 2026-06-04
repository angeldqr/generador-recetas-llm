<template>
  <article class="base-card">
    <slot />
  </article>
</template>

<style scoped>
.base-card {
  border: 1px solid rgb(15 36 24 / 0.08);
  border-radius: var(--radius-card);
  background:
    linear-gradient(155deg, rgb(254 253 248 / 0.96), rgb(236 240 226 / 0.88)),
    var(--color-panel);
  box-shadow: var(--shadow-card);
}
</style>
