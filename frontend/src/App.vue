<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import gsap from 'gsap'
import AppShell from './components/AppShell.vue'
import AuthPanel from './components/AuthPanel.vue'
import { useAuthSession } from './composables/useAuthSession'
import { useBlendy } from './composables/useBlendy'

const { isAuthenticated, clearSession, setToken } = useAuthSession()
const route = useRoute()
const router = useRouter()
const blendy = useBlendy()

/* ── Auth modal state (Blendy pattern) ── */
const showAuthModal = ref(false)
const activeBlendyId = ref('')

async function handleOpenAuth(blendyId: string) {
  if (showAuthModal.value) return
  activeBlendyId.value = blendyId
  showAuthModal.value = true
  await nextTick()
  blendy.update()
  blendy.toggle(blendyId)
}

function handleCloseAuth() {
  blendy.untoggle(activeBlendyId.value, () => {
    showAuthModal.value = false
    activeBlendyId.value = ''
  })
}

function handleAuthenticated(token: string) {
  setToken(token)
  blendy.untoggle(activeBlendyId.value, () => {
    showAuthModal.value = false
    activeBlendyId.value = ''
    const redirect = router.currentRoute.value.query.redirect
    const target = typeof redirect === 'string' ? redirect : '/inventario'
    void router.replace(target)
  })
}

function handleLogout() {
  clearSession()
}

/* ── Auto-open from ?auth=true query ── */
watch(
  () => route.query.auth,
  (val) => {
    if (val === 'true' && !isAuthenticated.value && !showAuthModal.value) {
      handleOpenAuth('auth-nav')
      void router.replace({ query: { ...route.query, auth: undefined } })
    }
  },
  { immediate: true },
)

/* ── Close modal if route changes ── */
watch(
  () => route.fullPath,
  () => {
    if (showAuthModal.value) {
      showAuthModal.value = false
      activeBlendyId.value = ''
    }
  },
)

/* ── Page transitions ── */
const isWelcome = computed(() => route.name === 'welcome')

function shouldReduceMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function onPageEnter(el: Element, done: () => void) {
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
      autoAlpha: 1, y: 0, filter: 'blur(0px)',
      duration: 0.36, ease: 'power3.out',
      clearProps: 'filter',
      onComplete: done,
    },
  )
}

function onPageLeave(el: Element, done: () => void) {
  const node = el as HTMLElement
  if (shouldReduceMotion()) {
    done()
    return
  }
  gsap.to(node, {
    autoAlpha: 0, y: -8, filter: 'blur(2px)',
    duration: 0.18, ease: 'power2.out',
    onComplete: done,
  })
}
</script>

<template>
  <AppShell
    :is-authenticated="isAuthenticated"
    @logout="handleLogout"
    @open-auth="handleOpenAuth"
  >
    <main class="page" :class="{ 'page--welcome': isWelcome }" data-app-root>
      <RouterView v-slot="{ Component }">
        <Transition :css="false" mode="out-in" @enter="onPageEnter" @leave="onPageLeave">
          <component :is="Component" :key="route.fullPath" @open-auth="handleOpenAuth" />
        </Transition>
      </RouterView>
    </main>
  </AppShell>

  <!-- Auth Modal — Blendy morph target via Teleport -->
  <Teleport to="body">
    <template v-if="showAuthModal">
      <div class="auth-backdrop" @click="handleCloseAuth"></div>
      <div class="auth-blendy-target" :data-blendy-to="activeBlendyId">
        <div class="auth-modal-card">
          <button
            class="auth-modal-close"
            type="button"
            aria-label="Cerrar"
            @click="handleCloseAuth"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
          <p class="auth-modal-eyebrow">Acceso</p>
          <h2 class="auth-modal-title">Bienvenido de vuelta</h2>
          <p class="auth-modal-hint">
            Inicia sesion para gestionar tu inventario y guardar recetas.
          </p>
          <AuthPanel @authenticated="handleAuthenticated" />
        </div>
      </div>
    </template>
  </Teleport>
</template>

<style>
/* ── Page wrapper ── */
.page {
  width: min(1240px, calc(100% - 32px));
  margin: 0 auto;
  padding: 32px 0 64px;
}

.page--welcome {
  width: 100%;
  padding: 0;
  overflow: hidden;
}

@media (max-width: 820px) {
  .page {
    width: min(100% - 24px, 720px);
    padding-top: 16px;
  }
  .page--welcome {
    width: 100%;
    padding: 0;
  }
}

/* ── Auth Backdrop ── */
.auth-backdrop {
  position: fixed;
  inset: 0;
  z-index: 999;
  background: rgb(15 36 24 / 0.35);
  -webkit-backdrop-filter: blur(14px) saturate(120%);
  backdrop-filter: blur(14px) saturate(120%);
  animation: auth-fade-in 0.3s ease forwards;
}

@keyframes auth-fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* ── Auth Blendy target — the element that morphs FROM the button ── */
.auth-blendy-target {
  position: fixed;
  inset: 0;
  width: fit-content;
  height: fit-content;
  margin: auto;
  z-index: 1000;
}

/* ── Auth modal card (single child of blendy target) ── */
.auth-modal-card {
  position: relative;
  display: grid;
  gap: 10px;
  width: min(520px, calc(100vw - 32px));
  padding: 40px 36px 36px;
  border: 1px solid rgb(15 36 24 / 0.08);
  border-radius: 32px;
  background:
    linear-gradient(160deg, rgb(254 253 248 / 0.98), rgb(244 241 232 / 0.94)),
    var(--color-panel);
  box-shadow:
    0 0 0 1px rgb(255 255 255 / 0.08),
    0 48px 120px -20px rgb(15 36 24 / 0.35),
    0 20px 50px -15px rgb(38 116 81 / 0.18);
}

.auth-modal-card::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  background:
    radial-gradient(ellipse at 20% -10%, rgb(255 255 255 / 0.7), transparent 55%);
  mix-blend-mode: lighten;
}

.auth-modal-close {
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
    background 180ms ease;
  z-index: 2;
}

.auth-modal-close:hover {
  color: var(--color-accent-strong);
  background: var(--color-accent-soft);
  transform: scale(1.05);
}

.auth-modal-close:active {
  transform: scale(0.9);
}

.auth-modal-eyebrow {
  margin: 0;
  color: var(--color-accent);
  font-family: "JetBrains Mono", monospace;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.auth-modal-title {
  margin: 0;
  font-family: "Bricolage Grotesque", system-ui;
  font-size: clamp(2rem, 4.5vw, 2.8rem);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.03em;
  color: var(--color-ink);
}

.auth-modal-hint {
  margin: 4px 0 8px;
  color: var(--color-muted);
  font-size: 0.95rem;
  line-height: 1.5;
  max-width: 38ch;
}

@media (max-width: 600px) {
  .auth-modal-card {
    padding: 32px 24px 28px;
  }
}
</style>