<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppShell from './components/AppShell.vue'
import { useAuthSession } from './composables/useAuthSession'

const { isAuthenticated, clearSession } = useAuthSession()

function handleLogout() {
  clearSession()
}
</script>

<template>
  <AppShell
    :is-authenticated="isAuthenticated"
    @logout="handleLogout"
  >
    <main class="page" data-app-root>
      <RouterView v-slot="{ Component, route }">
        <transition name="page" mode="out-in" appear>
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </RouterView>
    </main>
  </AppShell>
</template>

<style>
.page {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  padding: 32px 0 64px;
}

@media (max-width: 820px) {
  .page {
    width: min(100% - 24px, 680px);
    padding-top: 16px;
  }
}

.page-enter-active,
.page-leave-active {
  transition:
    opacity 280ms var(--ease-out),
    transform 320ms var(--ease-out),
    filter 280ms ease;
  will-change: opacity, transform, filter;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(14px);
  filter: blur(2px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-8px);
  filter: blur(2px);
}

@media (prefers-reduced-motion: reduce) {
  .page-enter-active,
  .page-leave-active {
    transition: opacity 0.01ms linear;
    filter: none !important;
  }

  .page-enter-from,
  .page-leave-to {
    transform: none;
    filter: none;
  }
}
</style>
