<script setup lang="ts">
import { computed, nextTick, onMounted, ref, type CSSProperties } from 'vue'
import { useRouter } from 'vue-router'
import gsap from 'gsap'
import { buildAnchoredBlendyTargetStyle } from '../composables/useAnchoredBlendyTarget'
import { useAppData } from '../composables/useAppData'
import { useAuthSession } from '../composables/useAuthSession'
import { useBlendy } from '../composables/useBlendy'

const { ingredients, recipes } = useAppData()
const { isAuthenticated } = useAuthSession()
const router = useRouter()
const blendy = useBlendy()

const emit = defineEmits<{
  'open-auth': [blendyId: string]
}>()

/* ── Flow modal state (Blendy) ── */
const showFlowModal = ref(false)
const flowTargetStyle = ref<CSSProperties>({})

async function openFlowModal() {
  flowTargetStyle.value = buildAnchoredBlendyTargetStyle('flow-info', {
    width: 560,
    height: 430,
  })
  showFlowModal.value = true
  await nextTick()
  blendy.update()
  blendy.toggle('flow-info')
}

function closeFlowModal() {
  blendy.untoggle('flow-info', () => {
    showFlowModal.value = false
    flowTargetStyle.value = {}
  })
}

/* ── Hero state ── */
const heroRoot = ref<HTMLElement | null>(null)
const heroLetters = 'cocina'.split('')

const heroEyebrow = 'Inventario inteligente'
const heroSubtitle = computed(() =>
  isAuthenticated.value
    ? 'Lo que ya tienes en la nevera se convierte en tu siguiente plato.'
    : 'Convierte lo que tienes en la nevera en una receta estructurada con IA.',
)

const primaryLabel = computed(() =>
  isAuthenticated.value ? 'Ir al inventario' : 'Empezar ahora',
)

function goToPrimary() {
  if (isAuthenticated.value) {
    void router.push({ name: 'inventory' })
    return
  }
  emit('open-auth', 'auth-cta')
}

/* ── Entrance animation ── */
function playEntrance() {
  if (!heroRoot.value) return
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduce) {
    gsap.set(heroRoot.value.querySelectorAll('[data-reveal]'), {
      autoAlpha: 1,
      y: 0,
    })
    return
  }

  gsap.context(() => {
    const letters = gsap.utils.toArray<HTMLElement>('.hero-letter')
    gsap.fromTo(
      letters,
      { autoAlpha: 0, y: 80, rotateX: -60 },
      {
        autoAlpha: 1, y: 0, rotateX: 0,
        duration: 1.0, ease: 'expo.out', stagger: 0.05,
      },
    )
    gsap.fromTo(
      '.hero-eyebrow',
      { autoAlpha: 0, y: 18, filter: 'blur(4px)' },
      { autoAlpha: 1, y: 0, filter: 'blur(0px)', duration: 0.7, ease: 'power3.out' },
    )
    gsap.fromTo(
      '.hero-subtitle',
      { autoAlpha: 0, y: 16 },
      { autoAlpha: 1, y: 0, duration: 0.7, ease: 'power3.out', delay: 0.55 },
    )
    gsap.fromTo(
      '.hero-actions',
      { autoAlpha: 0, y: 14 },
      { autoAlpha: 1, y: 0, duration: 0.6, ease: 'power3.out', delay: 0.7 },
    )
    gsap.fromTo(
      '.hero-summary',
      { autoAlpha: 0, y: 28, scale: 0.94, filter: 'blur(4px)' },
      {
        autoAlpha: 1, y: 0, scale: 1, filter: 'blur(0px)',
        duration: 0.9, ease: 'expo.out', delay: 0.85,
      },
    )
  }, heroRoot)
}

onMounted(() => {
  playEntrance()
  // Rescan blendy sources after mount (page is lazy-loaded)
  blendy.update()
})
</script>

<template>
  <article
    ref="heroRoot"
    class="welcome-root"
    data-route="welcome"
  >
    <section class="welcome-hero">
      <div class="welcome-hero__main">
        <p class="hero-eyebrow" data-reveal>
          <span class="hero-eyebrow__dot" aria-hidden="true"></span>
          {{ heroEyebrow }}
        </p>

        <h1 class="hero-title" aria-label="cocina">
          <span
            v-for="(letter, i) in heroLetters"
            :key="`${letter}-${i}`"
            class="hero-letter"
            :aria-hidden="true"
          >
            {{ letter }}
          </span>
        </h1>

        <p class="hero-subtitle" data-reveal>{{ heroSubtitle }}</p>

        <div class="hero-actions" data-reveal>
          <button
            class="cta cta--primary"
            type="button"
            data-blendy-from="auth-cta"
            @click="goToPrimary"
          >
            <span class="cta__inner">
              <span class="cta__label">{{ primaryLabel }}</span>
              <span class="cta__arrow" aria-hidden="true">
                <svg viewBox="0 0 16 16" width="16" height="16" fill="none">
                  <path
                    d="M3 8H13M13 8L8.5 3.5M13 8L8.5 12.5"
                    stroke="currentColor"
                    stroke-width="1.6"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </span>
            </span>
          </button>
          <button
            class="cta cta--ghost"
            type="button"
            data-blendy-from="flow-info"
            @click="openFlowModal"
          >
            <span class="cta__label">Ver como funciona</span>
          </button>
        </div>
      </div>

      <aside class="hero-summary" data-reveal aria-label="Resumen de la aplicacion">
        <div class="hero-summary__header">
          <span class="hero-summary__label">Tu cocina</span>
          <span class="hero-summary__status">
            <span class="hero-summary__pulse" aria-hidden="true"></span>
            en vivo
          </span>
        </div>
        <div class="hero-summary__row">
          <strong>{{ ingredients.length }}</strong>
          <span>ingredientes listos</span>
        </div>
        <div class="hero-summary__divider"></div>
        <div class="hero-summary__row">
          <strong>{{ recipes.length }}</strong>
          <span>recetas guardadas</span>
        </div>
        <p class="hero-summary__hint">
          Cada vez que generas una receta, el LLM usa exactamente lo que tienes.
        </p>
      </aside>
    </section>

    <!-- Flow Modal — Blendy morph from "Ver como funciona" button -->
    <Teleport to="body">
      <template v-if="showFlowModal">
        <div class="flow-backdrop" @click="closeFlowModal"></div>
        <div
          class="flow-blendy-target"
          data-blendy-to="flow-info"
          :style="flowTargetStyle"
        >
          <div class="flow-modal-card">
            <header class="flow-modal-header">
              <h2>Como funciona</h2>
              <button
                class="flow-modal-close"
                type="button"
                aria-label="Cerrar"
                @click="closeFlowModal"
              >
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </header>
            <ol class="modal-flow">
              <li><span>1</span>Crear cuenta o iniciar sesion</li>
              <li><span>2</span>Registrar ingredientes disponibles</li>
              <li><span>3</span>Generar receta estructurada con IA</li>
              <li><span>4</span>Guardar, calificar o eliminar del historial</li>
            </ol>
          </div>
        </div>
      </template>
    </Teleport>
  </article>
</template>

<style scoped>
.welcome-root {
  height: 100%;
  width: min(1240px, 100%);
  margin: 0 auto;
  perspective: 1200px;
  overflow: hidden;
}

.welcome-hero {
  height: 100%;
  max-height: 100%;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, 420px);
  gap: clamp(28px, 5vw, 64px);
  align-items: center;
  padding: clamp(14px, 3vh, 34px) 0;
  overflow: hidden;
}

.welcome-hero__main {
  display: grid;
  gap: clamp(14px, 2.7vh, 28px);
}

/* ── Eyebrow ── */
.hero-eyebrow {
  margin: 0;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
  padding: 8px 16px 8px 12px;
  border: 1px solid rgb(15 36 24 / 0.1);
  border-radius: var(--radius-button);
  color: var(--color-ink);
  background: rgb(254 253 248 / 0.7);
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 0.74rem;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  box-shadow: 0 8px 24px -16px rgb(15 36 24 / 0.3);
}

.hero-eyebrow__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-accent);
  box-shadow: 0 0 0 4px rgb(38 116 81 / 0.18);
}

/* ── Title ── */
.hero-title {
  margin: 0;
  font-family: "Bricolage Grotesque", system-ui, serif;
  font-weight: 700;
  font-size: clamp(5rem, min(18vw, 24vh), 16rem);
  line-height: 0.82;
  letter-spacing: -0.04em;
  color: var(--color-ink);
  display: flex;
  flex-wrap: wrap;
  transform-style: preserve-3d;
  text-transform: lowercase;
}

.hero-letter {
  display: inline-block;
  cursor: default;
  user-select: none;
  transform-origin: 50% 80%;
  transition:
    font-weight 280ms var(--ease-out),
    transform 320ms var(--ease-out),
    color 320ms ease,
    margin 280ms var(--ease-out),
    text-shadow 320ms ease;
  will-change: transform;
}

.hero-letter:hover {
  font-weight: 800;
  transform: translateY(-6px) scale(1.06);
  color: var(--color-accent);
  margin: 0 6px;
  text-shadow: 0 12px 32px rgb(38 116 81 / 0.32);
}

/* ── Subtitle ── */
.hero-subtitle {
  margin: 0;
  max-width: 56ch;
  color: var(--color-ink-soft);
  font-family: "DM Sans", system-ui;
  font-size: clamp(1rem, min(1.6vw, 2.8vh), 1.35rem);
  line-height: 1.5;
  letter-spacing: -0.01em;
}

/* ── CTA buttons ── */
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 2px;
}

.cta {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  min-height: 54px;
  padding: 0 28px;
  border-radius: var(--radius-button);
  font-family: "DM Sans", system-ui;
  font-weight: 700;
  font-size: 0.98rem;
  letter-spacing: -0.01em;
  transition:
    transform 200ms var(--ease-out),
    box-shadow 200ms ease,
    background 200ms ease,
    color 200ms ease;
}

.cta__inner {
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.cta--primary {
  color: var(--color-panel);
  background:
    linear-gradient(180deg, #3a8a64, var(--color-accent) 78%),
    var(--color-accent);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.18),
    0 22px 50px -16px rgb(38 116 81 / 0.55);
}

.cta--ghost {
  color: var(--color-ink);
  background: var(--color-panel);
  box-shadow:
    inset 0 0 0 1px rgb(15 36 24 / 0.1),
    0 14px 30px -18px rgb(15 36 24 / 0.18);
}

.cta__arrow {
  display: inline-grid;
  place-items: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgb(255 255 255 / 0.18);
  color: inherit;
  transition: transform 220ms var(--ease-out);
}

.cta--primary .cta__arrow {
  background: rgb(255 255 255 / 0.22);
}

.cta:active {
  transform: scale(0.97);
}

@media (hover: hover) and (pointer: fine) {
  .cta--primary:hover {
    transform: translateY(-1px);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / 0.2),
      0 28px 60px -16px rgb(38 116 81 / 0.6);
  }

  .cta--primary:hover .cta__arrow {
    transform: translateX(3px);
  }

  .cta--ghost:hover {
    transform: translateY(-1px);
    background: var(--color-soft-2);
  }
}

/* ── Summary card ── */
.hero-summary {
  display: grid;
  gap: 14px;
  padding: 28px;
  border: 1px solid rgb(15 36 24 / 0.08);
  border-radius: var(--radius-card);
  background:
    linear-gradient(160deg, rgb(254 253 248 / 0.92), rgb(244 241 232 / 0.88)),
    var(--color-panel);
  box-shadow: var(--shadow-card);
  -webkit-backdrop-filter: blur(18px);
  backdrop-filter: blur(18px);
  transform-origin: center;
}

.hero-summary__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--color-muted);
  font-family: "JetBrains Mono", monospace;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.hero-summary__status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--color-accent-strong);
}

.hero-summary__pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-accent);
  box-shadow: 0 0 0 0 rgb(38 116 81 / 0.5);
  animation: pulse 2.2s ease-out infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgb(38 116 81 / 0.45); }
  70% { box-shadow: 0 0 0 12px rgb(38 116 81 / 0); }
  100% { box-shadow: 0 0 0 0 rgb(38 116 81 / 0); }
}

.hero-summary__row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.hero-summary__row strong {
  font-family: "Bricolage Grotesque", system-ui;
  font-size: 2.4rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.03em;
  color: var(--color-ink);
}

.hero-summary__row span {
  color: var(--color-muted);
  font-size: 0.92rem;
  text-align: right;
}

.hero-summary__divider {
  height: 1px;
  background: var(--color-line);
  margin: 4px 0;
}

.hero-summary__hint {
  margin: 6px 0 0;
  color: var(--color-muted);
  font-size: 0.82rem;
  line-height: 1.5;
}

/* ── Flow modal (Blendy target) ── */
.flow-backdrop {
  position: fixed;
  inset: 0;
  z-index: 999;
  background: rgb(15 36 24 / 0.35);
  -webkit-backdrop-filter: blur(14px) saturate(120%);
  backdrop-filter: blur(14px) saturate(120%);
  animation: flow-fade-in 0.28s var(--ease-out) forwards;
}

@keyframes flow-fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.flow-blendy-target {
  position: fixed;
  right: auto;
  bottom: auto;
  height: fit-content;
  z-index: 1000;
  transform-origin: var(--blendy-origin-x, 50%) var(--blendy-origin-y, 50%);
}

.flow-modal-card {
  position: relative;
  width: 100%;
  max-height: inherit;
  overflow: auto;
  border: 1px solid rgb(15 36 24 / 0.08);
  border-radius: 32px;
  background:
    linear-gradient(160deg, rgb(254 253 248 / 0.98), rgb(244 241 232 / 0.94)),
    var(--color-panel);
  box-shadow:
    0 0 0 1px rgb(255 255 255 / 0.08),
    0 48px 120px -20px rgb(15 36 24 / 0.35),
    0 20px 50px -15px rgb(38 116 81 / 0.18);
  transform-origin: var(--blendy-origin-x, 50%) var(--blendy-origin-y, 50%);
}

.flow-modal-card::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  background:
    radial-gradient(circle at 20% 0%, rgb(255 255 255 / 0.7), transparent 50%);
  mix-blend-mode: lighten;
}

.flow-modal-header {
  display: flex;
  gap: 18px;
  align-items: start;
  justify-content: space-between;
  padding: 28px 28px 0;
}

.flow-modal-header h2 {
  margin: 0;
  font-family: "Bricolage Grotesque", system-ui;
  font-size: clamp(2rem, 4vw, 2.6rem);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.025em;
  color: var(--color-ink);
}

.flow-modal-close {
  width: 44px;
  height: 44px;
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  border: 1px solid rgb(15 36 24 / 0.1);
  border-radius: 50%;
  color: var(--color-ink);
  background: var(--color-panel);
  line-height: 1;
  transition:
    transform 160ms var(--ease-out),
    color 180ms ease,
    background 180ms ease;
}

.flow-modal-close:hover {
  color: var(--color-accent-strong);
  background: var(--color-accent-soft);
}

.flow-modal-close:active {
  transform: scale(0.92);
}

.modal-flow {
  display: grid;
  gap: 10px;
  margin: 0;
  padding: 18px 28px 28px;
  list-style: none;
}

.modal-flow li {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 14px;
  align-items: center;
  padding: 14px 16px;
  color: var(--color-ink);
  background: var(--color-soft);
  border: 1px solid rgb(15 36 24 / 0.06);
  border-radius: 18px;
  font-weight: 600;
  font-size: 0.95rem;
  letter-spacing: -0.005em;
}

.modal-flow span {
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: var(--color-panel);
  background:
    linear-gradient(180deg, #3a8a64, var(--color-accent) 80%),
    var(--color-accent);
  font-family: "Bricolage Grotesque", system-ui;
  font-size: 0.95rem;
  font-weight: 700;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.2),
    0 8px 18px -8px rgb(38 116 81 / 0.5);
}

/* ── Responsive ── */
@media (max-width: 980px) {
  .welcome-hero {
    grid-template-columns: 1fr;
    gap: 22px;
  }
  .hero-summary {
    order: 2;
    padding: 20px;
  }
}

@media (max-width: 600px) {
  .welcome-hero {
    align-content: center;
  }

  .hero-title {
    font-size: clamp(4rem, min(25vw, 20vh), 8rem);
  }

  .hero-summary {
    display: none;
  }

  .cta {
    flex: 1;
    justify-content: center;
  }
}

@media (max-height: 760px) and (min-width: 981px) {
  .hero-eyebrow {
    padding-block: 6px;
  }

  .hero-summary {
    gap: 10px;
    padding: 22px;
  }

  .hero-summary__hint {
    display: none;
  }

  .cta {
    min-height: 50px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .flow-backdrop {
    animation: none;
  }
}
</style>
