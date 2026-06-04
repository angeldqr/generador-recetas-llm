<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue'
import gsap from 'gsap'
import { Flip } from 'gsap/Flip'
import { CustomEase } from 'gsap/CustomEase'
import { PrettyModal } from 'prettier-modals'

gsap.registerPlugin(Flip, CustomEase)

const props = defineProps<{
  open: boolean
  title: string
  blendyId?: string
}>()

const emit = defineEmits<{
  close: []
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
  if (!props.blendyId) return undefined
  const trigger = document.querySelector<HTMLElement>(
    `[data-blendy-from="${props.blendyId}"]`,
  )
  return trigger ?? undefined
}

async function openDialog() {
  if (!dialog.value) return

  if (shouldReduceMotion()) {
    if (!dialog.value.open) dialog.value.showModal()
    gsap.set(dialog.value, { autoAlpha: 1 })
    return
  }

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
  if (!dialog.value || !dialog.value.open) return

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

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
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
            ×
          </button>
        </header>
        <div class="base-modal__body">
          <slot />
        </div>
      </div>
    </article>
  </dialog>
</template>
