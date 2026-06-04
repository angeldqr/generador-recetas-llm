<script setup lang="ts">
import { onBeforeUnmount, ref, watch, nextTick } from 'vue'
import gsap from 'gsap'
import { Flip } from 'gsap/Flip'
import { CustomEase } from 'gsap/CustomEase'
import { PrettyModal } from 'prettier-modals'
import AuthPanel from './AuthPanel.vue'

gsap.registerPlugin(Flip, CustomEase)

const props = defineProps<{
  open: boolean
  triggerSelector?: string
}>()

const emit = defineEmits<{
  close: []
  authenticated: [token: string]
}>()

const dialog = ref<HTMLDialogElement | null>(null)
const ELASTIC_EASE = 'M0,0 C0.4,0 0.2,1 0.6,1 0.8,1 1,1 1,1'

const prettyModal = new PrettyModal({
  anchor: 'origin',
  duration: 0.7,
  ease: ELASTIC_EASE,
  respectReducedMotion: true,
})

function shouldReduceMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function resolveTrigger(): HTMLElement | undefined {
  if (!props.triggerSelector) return undefined
  const trigger = document.querySelector<HTMLElement>(props.triggerSelector)
  return trigger ?? undefined
}

async function openDialog() {
  if (!dialog.value) return

  const trigger = resolveTrigger()
  if (trigger) {
    prettyModal.open(dialog.value, {
      trigger,
      anchor: 'origin',
      duration: 0.7,
    })
  } else {
    prettyModal.open(dialog.value, {
      anchor: 'center',
      duration: 0.7,
    })
  }
}

function closeDialog() {
  if (!dialog.value || !dialog.value.open) {
    emit('close')
    return
  }

  if (shouldReduceMotion()) {
    dialog.value.close()
    return
  }

  prettyModal.close(dialog.value, { duration: 0.4 })
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

onBeforeUnmount(() => {
  prettyModal.destroy()
})
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
}

.auth-modal::backdrop {
  background: rgb(15 36 24 / 0.45);
  -webkit-backdrop-filter: blur(20px) saturate(140%);
  backdrop-filter: blur(20px) saturate(140%);
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
  will-change: transform, opacity;
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
    transform 180ms var(--ease-out),
    color 180ms ease,
    border-color 180ms ease,
    background 180ms ease;
  z-index: 2;
}

.auth-modal__close:active {
  transform: scale(0.9);
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
  .auth-modal__card {
    transform: none !important;
  }
}
</style>
