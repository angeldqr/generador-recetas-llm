<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'

const props = defineProps<{
  open: boolean
  title: string
  blendyId?: string
}>()

const emit = defineEmits<{
  close: []
}>()

const dialog = ref<HTMLDialogElement | null>(null)
const isClosing = ref(false)

const DURATION = 400

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
  if (!dialog.value || !dialog.value.open || isClosing.value) return
  isClosing.value = true

  if (shouldReduceMotion()) {
    dialog.value.close()
    isClosing.value = false
    return
  }

  setTimeout(() => {
    if (dialog.value) {
      dialog.value.close()
      isClosing.value = false
    }
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
    class="base-modal"
    :data-blendy-to="blendyId || undefined"
    role="document"
    @cancel="onCancel"
    @close="onClose"
    @click="onClick"
  >
    <article class="base-modal__card">
      <div class="base-modal__surface">
        <header class="base-modal__header">
          <h2>{{ title }}</h2>
          <button
            class="base-modal__close"
            type="button"
            aria-label="Cerrar modal"
            @click="closeDialog"
          >
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </header>
        <div class="base-modal__body">
          <slot />
        </div>
      </div>
    </article>
  </dialog>
</template>
