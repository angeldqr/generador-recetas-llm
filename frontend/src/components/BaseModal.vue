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

const overlay = ref<HTMLDivElement | null>(null)
const isClosing = ref(false)
const isOpen = ref(false)

const DURATION = 350

function shouldReduceMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

async function openModal() {
  if (isOpen.value) return
  isClosing.value = false
  isOpen.value = true
  document.body.style.overflow = 'hidden'
}

function closeModal() {
  if (!isOpen.value || isClosing.value) return
  isClosing.value = true

  if (shouldReduceMotion()) {
    isOpen.value = false
    isClosing.value = false
    document.body.style.overflow = ''
    emit('close')
    return
  }

  setTimeout(() => {
    isOpen.value = false
    isClosing.value = false
    document.body.style.overflow = ''
    emit('close')
  }, DURATION)
}

function onClickOverlay(event: MouseEvent) {
  if (event.target === overlay.value) {
    closeModal()
  }
}

watch(
  () => props.open,
  async (isOpenProp) => {
    if (isOpenProp) {
      await nextTick()
      void openModal()
    } else {
      closeModal()
    }
  },
  { immediate: true },
)
</script>

<template>
  <div
    v-if="isOpen || isClosing"
    ref="overlay"
    class="base-modal"
    :class="{ 'is-closing': isClosing }"
    role="dialog"
    aria-modal="true"
    @click="onClickOverlay"
  >
    <article class="base-modal__card">
      <div class="base-modal__surface">
        <header class="base-modal__header">
          <h2>{{ title }}</h2>
          <button
            class="base-modal__close"
            type="button"
            aria-label="Cerrar modal"
            @click="closeModal"
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
  </div>
</template>
