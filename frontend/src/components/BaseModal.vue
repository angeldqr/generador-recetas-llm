<script setup lang="ts">
import gsap from 'gsap'
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import type { Blendy } from 'blendy'

const props = defineProps<{
  open: boolean
  title: string
  blendyId?: string
}>()

const emit = defineEmits<{
  close: []
}>()

const dialog = ref<HTMLDialogElement | null>(null)
const modalCard = ref<HTMLElement | null>(null)
const modalState = ref<'closed' | 'open' | 'closing'>('closed')
let blendyInstance: Blendy | null = null
let blendyUnavailable = false

function shouldReduceMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function cancelMotion() {
  if (modalCard.value) {
    gsap.killTweensOf(modalCard.value)
  }
}

async function getBlendy() {
  if (!props.blendyId || blendyUnavailable) {
    return null
  }

  if (blendyInstance) {
    return blendyInstance
  }

  try {
    const blendyModule = await import('blendy')
    const create = blendyModule.createBlendy

    if (!create) {
      blendyUnavailable = true
      return null
    }

    blendyInstance = create({ animation: 'dynamic' })
    return blendyInstance
  } catch {
    blendyUnavailable = true
    return null
  }
}

async function runOpenMotion() {
  modalState.value = 'open'

  if (shouldReduceMotion() || !modalCard.value) {
    return
  }

  const blendy = await getBlendy()

  if (blendy && props.blendyId) {
    await nextTick()
    blendy.update()
    blendy.toggle(props.blendyId)
  }

  gsap.fromTo(
    modalCard.value,
    {
      autoAlpha: 0,
      filter: 'blur(3px)',
      scale: 0.97,
      y: 10,
    },
    {
      autoAlpha: 1,
      duration: 0.24,
      ease: 'power3.out',
      filter: 'blur(0px)',
      overwrite: true,
      scale: 1,
      y: 0,
    },
  )
}

function finishClose() {
  dialog.value?.close()
  modalState.value = 'closed'
}

async function openDialog() {
  cancelMotion()

  if (!dialog.value?.open) {
    dialog.value?.showModal()
  }

  await nextTick()
  void runOpenMotion()
}

async function closeDialog() {
  if (!dialog.value?.open || modalState.value === 'closing') {
    return
  }

  modalState.value = 'closing'

  if (shouldReduceMotion() || !modalCard.value) {
    finishClose()
    return
  }

  const blendy = await getBlendy()

  gsap.to(modalCard.value, {
    autoAlpha: 0,
    duration: 0.16,
    ease: 'power2.out',
    filter: 'blur(2px)',
    overwrite: true,
    scale: 0.97,
    y: 8,
    onComplete: () => {
      if (blendy && props.blendyId) {
        blendy.untoggle(props.blendyId, finishClose)
      } else {
        finishClose()
      }
    },
  })
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
  cancelMotion()
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
    <article
      ref="modalCard"
      class="base-modal__card"
      :data-blendy-to="blendyId"
      role="document"
    >
      <div class="base-modal__surface">
        <header class="base-modal__header">
          <h2>{{ title }}</h2>
          <button class="base-modal__close" type="button" aria-label="Cerrar modal" @click="requestClose">
            x
          </button>
        </header>
        <div class="base-modal__body">
          <slot />
        </div>
      </div>
    </article>
  </dialog>
</template>
