<script setup lang="ts">
withDefaults(
  defineProps<{
    type?: 'button' | 'submit' | 'reset'
    variant?: 'solid' | 'soft' | 'danger'
    disabled?: boolean
  }>(),
  {
    type: 'button',
    variant: 'solid',
    disabled: false,
  },
)
</script>

<template>
  <button
    class="base-button"
    :class="`base-button--${variant}`"
    :disabled="disabled"
    :type="type"
  >
    <slot />
  </button>
</template>

<style scoped>
.base-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-height: 48px;
  padding: 0 22px;
  border: 0;
  border-radius: var(--radius-button);
  font-family: "DM Sans", system-ui;
  font-size: 0.95rem;
  font-weight: 800;
  letter-spacing: 0;
  cursor: pointer;
  transition:
    background 180ms ease,
    box-shadow 180ms ease,
    color 180ms ease,
    transform 180ms var(--ease-out);
}

.base-button:disabled {
  cursor: not-allowed;
  opacity: 0.62;
}

.base-button--solid {
  color: var(--color-panel);
  background:
    linear-gradient(180deg, #3a8a64, var(--color-accent) 78%),
    var(--color-accent);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.18),
    0 18px 40px -12px rgb(38 116 81 / 0.5);
}

.base-button--soft {
  color: var(--color-ink);
  background: var(--color-panel);
  box-shadow:
    inset 0 0 0 1px rgb(15 36 24 / 0.1),
    0 10px 24px -16px rgb(15 36 24 / 0.18);
}

.base-button--danger {
  color: var(--color-danger);
  background: var(--color-panel);
  box-shadow:
    inset 0 0 0 1px rgb(163 61 61 / 0.18),
    0 10px 24px -16px rgb(15 36 24 / 0.18);
}

.base-button:active {
  transform: scale(0.97);
}

@media (hover: hover) and (pointer: fine) {
  .base-button:not(:disabled):hover {
    transform: translateY(-1px);
  }

  .base-button--solid:not(:disabled):hover {
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / 0.2),
      0 22px 50px -12px rgb(38 116 81 / 0.55);
  }

  .base-button--soft:not(:disabled):hover {
    background: var(--color-soft-2);
  }

  .base-button--danger:not(:disabled):hover {
    background: rgb(163 61 61 / 0.08);
  }
}
</style>
