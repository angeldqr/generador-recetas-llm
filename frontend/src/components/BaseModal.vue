<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps<{
  open: boolean
  title: string
}>()

const emit = defineEmits<{
  close: []
}>()

const dialog = ref<HTMLDialogElement | null>(null)
const modalState = ref<'closed' | 'open' | 'closing'>('closed')
let closeTimer: number | undefined

function clearCloseTimer() {
  if (closeTimer) {
    window.clearTimeout(closeTimer)
    closeTimer = undefined
  }
}

function openDialog() {
  clearCloseTimer()

  if (!dialog.value?.open) {
    dialog.value?.showModal()
  }

  requestAnimationFrame(() => {
    modalState.value = 'open'
  })
}

function closeDialog() {
  if (!dialog.value?.open || modalState.value === 'closing') {
    return
  }

  modalState.value = 'closing'
  closeTimer = window.setTimeout(() => {
    dialog.value?.close()
    modalState.value = 'closed'
  }, 220)
}

function requestClose() {
  emit('close')
}

function handleCancel(event: Event) {
  event.preventDefault()
  requestClose()
}

function handleDialogClick(event: MouseEvent) {
  if (event.target === dialog.value) {
    requestClose()
  }
}

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      openDialog()
    } else {
      closeDialog()
    }
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  clearCloseTimer()
})
</script>

<template>
  <dialog
    ref="dialog"
    class="base-modal"
    :data-state="modalState"
    @cancel="handleCancel"
    @click="handleDialogClick"
  >
    <article class="base-modal__card" role="document">
      <header class="base-modal__header">
        <h2>{{ title }}</h2>
        <button class="base-modal__close" type="button" aria-label="Cerrar modal" @click="requestClose">
          ×
        </button>
      </header>
      <div class="base-modal__body">
        <slot />
      </div>
    </article>
  </dialog>
</template>
