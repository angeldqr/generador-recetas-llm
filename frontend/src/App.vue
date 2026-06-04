<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import gsap from 'gsap'
import AppShell from './components/AppShell.vue'
import { useAuthSession } from './composables/useAuthSession'

const { isAuthenticated, clearSession } = useAuthSession()
const route = useRoute()

function handleLogout() {
  clearSession()
}

function shouldReduceMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function supportsViewTransitions(): boolean {
  if (typeof document === 'undefined') return false
  return typeof (document as Document & { startViewTransition?: unknown })
    .startViewTransition === 'function'
}

function onPageEnter(el: Element, done: () => void) {
  // If the browser is doing the View Transition, let it own the swap.
  if (supportsViewTransitions()) {
    done()
    return
  }
  const node = el as HTMLElement
  if (shouldReduceMotion()) {
    gsap.set(node, { autoAlpha: 1, y: 0, filter: 'blur(0px)' })
    done()
    return
  }
  gsap.fromTo(
    node,
    { autoAlpha: 0, y: 14, filter: 'blur(2px)' },
    {
      autoAlpha: 1,
      y: 0,
      filter: 'blur(0px)',
      duration: 0.36,
      ease: 'power3.out',
      clearProps: 'filter',
      onComplete: done,
    },
  )
}

function onPageLeave(el: Element, done: () => void) {
  if (supportsViewTransitions()) {
    done()
    return
  }
  const node = el as HTMLElement
  if (shouldReduceMotion()) {
    done()
    return
  }
  gsap.to(node, {
    autoAlpha: 0,
    y: -8,
    filter: 'blur(2px)',
    duration: 0.18,
    ease: 'power2.out',
    onComplete: done,
  })
}
</script>

<template>
  <AppShell
    :is-authenticated="isAuthenticated"
    @logout="handleLogout"
  >
    <main class="page" data-app-root>
      <RouterView v-slot="{ Component }">
        <Transition
          :css="false"
          mode="out-in"
          @enter="onPageEnter"
          @leave="onPageLeave"
        >
          <component :is="Component" :key="route.fullPath" />
        </Transition>
      </RouterView>
    </main>
  </AppShell>
</template>

<style>
.page {
  width: min(1240px, calc(100% - 32px));
  margin: 0 auto;
  padding: 32px 0 64px;
}

@media (max-width: 820px) {
  .page {
    width: min(100% - 24px, 720px);
    padding-top: 16px;
  }
}
</style>
