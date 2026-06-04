<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import AuthPanel from './AuthPanel.vue'

const props = defineProps<{
  open: boolean
  triggerSelector?: string
}>()

const emit = defineEmits<{
  close: []
  authenticated: [token: string]
}>()

const dialog = ref<HTMLDialogElement | null>(null)
const isClosing = ref(false)

const DURATION = 420

function shouldReduceMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

async function openDialog() {
  if (!dialog.value) return
  if (dialog.value.open) return

  isClosing.value = false
  dialog.value.showModal()
}

function closeDialog() {
  if (!dialog.value || !dialog.value.open || isClosing.value) {
    emit('close')
    return
  }
  isClosing.value = true

  if (shouldReduceMotion()) {
    dialog.value.close()
    isClosing.value = false
    emit('close')
    return
  }

  setTimeout(() => {
    if (dialog.value) {
      dialog.value.close()
    }
    isClosing.value = false
    emit('close')
  }, DURATION)
}

function onCancel(event: Event) {
  event.preventDefault()
  closeDialog()
}

function onClick(event: MouseEvent) {
  if (event.target === dialog.value) {
    closeDialog()
  }
}

function onClose() {
  emit('close')
}

function handleAuthenticated(token: string) {
  emit('authenticated', token)
}

watch(
  () => props.open,
  async (isOpen) => {
    if (isOpen) {
      await nextTick()
      void openDialog()
    } else {
      closeDialog()
    }
  },
  { immediate: true },
)
</script>

<template>
  <dialog
    ref="dialog"
    class="auth-modal"
    role="document"
    @cancel="onCancel"
    @close="onClose"
    @click="onClick"
  >
    <article class="auth-modal__card">
      <div class="auth-modal__surface">
        <button
          class="auth-modal__close"
          type="button"
          aria-label="Cerrar modal"
          @click="closeDialog"
        >
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        <div class="auth-modal__header">
          <p class="auth-modal__eyebrow">Acceso</p>
          <h2 class="auth-modal__title">Bienvenido<br>de vuelta</h2>
          <p class="auth-modal__hint">
            Inicia sesion para gestionar tu inventario y guardar recetas.
          </p>
        </div>

        <div class="auth-modal__body">
          <AuthPanel @authenticated="handleAuthenticated" />
        </div>
      </div>
    </article>
  </dialog>
</template>

<style scoped>
.auth-modal {
  width: min(520px, calc(100% - 32px));
  max-width: 520px;
  border: 0;
  padding: 0;
  color: var(--color-ink);
  background: transparent;
  overflow: visible;
  opacity: 0;
  visibility: hidden;
  transition:
    opacity 320ms cubic-bezier(0.23, 1, 0.32, 1),
    visibility 0ms 320ms;
  will-change: opacity, visibility;
}

.auth-modal[open] {
  opacity: 1;
  visibility: visible;
  transition:
    opacity 320ms cubic-bezier(0.23, 1, 0.32, 1),
    visibility 0ms 0ms;
}

.auth-modal::backdrop {
  background: rgb(15 36 24 / 0.55);
  opacity: 0;
  transition: opacity 320ms cubic-bezier(0.23, 1, 0.32, 1);
}

.auth-modal[open]::backdrop {
  opacity: 1;
}

.auth-modal__card {
  position: relative;
  overflow: hidden;
  border: 1px solid rgb(15 36 24 / 0.08);
  border-radius: 32px;
  background:
    linear-gradient(160deg, rgb(254 253 248 / 0.98), rgb(244 241 232 / 0.94)),
    var(--color-panel);
  box-shadow:
    0 0 0 1px rgb(255 255 255 / 0.1),
    0 48px 120px -20px rgb(15 36 24 / 0.35),
    0 20px 50px -15px rgb(38 116 81 / 0.2);
  transform-origin: center;
  transform: scale(0.94) translateY(12px);
  opacity: 0;
  transition:
    transform 420ms cubic-bezier(0.34, 1.56, 0.64, 1),
    opacity 320ms cubic-bezier(0.23, 1, 0.32, 1);
  will-change: transform, opacity;
}

.auth-modal[open] .auth-modal__card {
  transform: scale(1) translateY(0);
  opacity: 1;
}

.auth-modal__card::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  background:
    radial-gradient(
      ellipse at 20% -10%,
      rgb(255 255 255 / 0.8),
      transparent 55%
    ),
    radial-gradient(
      circle at 90% 100%,
      rgb(38 116 81 / 0.06),
      transparent 40%
    );
  mix-blend-mode: lighten;
}

.auth-modal__surface {
  position: relative;
  border-radius: inherit;
  padding: 40px 36px 36px;
}

.auth-modal__close {
  position: absolute;
  top: 16px;
  right: 16px;
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border: 1px solid rgb(15 36 24 / 0.08);
  border-radius: 50%;
  color: var(--color-muted);
  background: rgb(254 253 248 / 0.7);
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);
  transition:
    transform 280ms cubic-bezier(0.34, 1.56, 0.64, 1),
    color 180ms ease,
    border-color 180ms ease,
    background 180ms ease;
  will-change: transform;
  z-index: 2;
}

.auth-modal__close:active {
  transform: scale(0.92);
  transition-duration: 120ms;
}

.auth-modal__header {
  display: grid;
  gap: 10px;
  margin-bottom: 24px;
}

.auth-modal__eyebrow {
  margin: 0;
  color: var(--color-accent);
  font-family: "JetBrains Mono", monospace;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.auth-modal__title {
  margin: 0;
  font-family: "Bricolage Grotesque", system-ui;
  font-size: clamp(2rem, 4.5vw, 2.8rem);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.03em;
  color: var(--color-ink);
}

.auth-modal__hint {
  margin: 4px 0 0;
  color: var(--color-muted);
  font-size: 0.95rem;
  line-height: 1.5;
  max-width: 38ch;
}

.auth-modal__body {
  position: relative;
}

@media (hover: hover) and (pointer: fine) {
  .auth-modal__close:hover {
    color: var(--color-accent-strong);
    border-color: rgb(38 116 81 / 0.25);
    background: var(--color-accent-soft);
    transform: scale(1.05);
  }
}

@media (max-width: 600px) {
  .auth-modal__surface {
    padding: 32px 24px 28px;
  }

  .auth-modal__title {
    font-size: 2rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .auth-modal,
  .auth-modal::backdrop,
  .auth-modal__card {
    transition: none !important;
    transform: none !important;
    opacity: 1 !important;
    visibility: visible !important;
  }
}
</style>
