<script setup lang="ts">
import { computed, nextTick, onMounted, ref, type CSSProperties } from 'vue'
import { useRouter } from 'vue-router'
import gsap from 'gsap'
import { buildAnchoredBlendyTargetStyle } from '../composables/useAnchoredBlendyTarget'
import { useAuthSession } from '../composables/useAuthSession'
import { useBlendy } from '../composables/useBlendy'

const { isAuthenticated } = useAuthSession()
const router = useRouter()
const blendy = useBlendy()

const emit = defineEmits<{
  'open-auth': [blendyId: string]
}>()

const showFlowModal = ref(false)
const flowTargetStyle = ref<CSSProperties>({})
const heroRoot = ref<HTMLElement | null>(null)
const heroLetters = 'cocina'.split('')

const heroSubtitle = computed(() =>
  isAuthenticated.value
    ? 'Abre tu inventario, ajusta ingredientes y genera una receta cuando quieras probar combinaciones.'
    : 'Guarda ingredientes, genera una propuesta y conserva el historial sin promesas infladas.',
)

const primaryLabel = computed(() =>
  isAuthenticated.value ? 'Ir al inventario' : 'Empezar ahora',
)

async function openFlowModal() {
  flowTargetStyle.value = buildAnchoredBlendyTargetStyle('flow-info', {
    width: 560,
    height: 430,
    margin: 18,
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

function goToPrimary() {
  if (isAuthenticated.value) {
    void router.push({ name: 'inventory' })
    return
  }
  emit('open-auth', 'auth-cta')
}

function playEntrance() {
  if (!heroRoot.value) return
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  if (reduce) {
    gsap.set(heroRoot.value.querySelectorAll('[data-reveal], .hero-letter'), {
      autoAlpha: 1,
      y: 0,
      x: 0,
      rotateX: 0,
    })
    return
  }

  gsap.context(() => {
    gsap.fromTo(
      '.hero-letter',
      { autoAlpha: 0, y: 76, rotateX: -58 },
      {
        autoAlpha: 1,
        y: 0,
        rotateX: 0,
        duration: 1.05,
        ease: 'expo.out',
        stagger: 0.045,
      },
    )
    gsap.fromTo(
      '[data-reveal]',
      { autoAlpha: 0, y: 20, scale: 0.98 },
      {
        autoAlpha: 1,
        y: 0,
        scale: 1,
        duration: 0.72,
        ease: 'power3.out',
        stagger: 0.08,
        delay: 0.38,
      },
    )
    gsap.fromTo(
      '.hero-proof',
      { autoAlpha: 0, x: 28 },
      {
        autoAlpha: 1,
        x: 0,
        duration: 0.9,
        ease: 'expo.out',
        delay: 0.62,
      },
    )
    gsap.fromTo(
      '.cta--primary',
      { autoAlpha: 0, scale: 0.92, y: 12 },
      {
        autoAlpha: 1,
        scale: 1,
        y: 0,
        duration: 0.6,
        ease: 'back.out(1.7)',
        delay: 0.55,
      }
    )
    gsap.fromTo(
      '.cta--ghost',
      { autoAlpha: 0, scale: 0.92, y: 12 },
      {
        autoAlpha: 1,
        scale: 1,
        y: 0,
        duration: 0.6,
        ease: 'back.out(1.7)',
        delay: 0.65,
      }
    )
  }, heroRoot)
}

onMounted(() => {
  playEntrance()
  blendy.update()
})
</script>

<template>
  <article ref="heroRoot" class="welcome-root" data-route="welcome">
    <section class="welcome-hero">
      <div class="welcome-hero__main">
        <p class="hero-eyebrow" data-reveal>
          <span class="hero-eyebrow__dot" aria-hidden="true"></span>
          Recetas LLM
        </p>

        <h1 class="hero-title" aria-label="cocina">
          <span
            v-for="(letter, i) in heroLetters"
            :key="`${letter}-${i}`"
            class="hero-letter"
            aria-hidden="true"
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
            <span class="cta__label">Ver flujo</span>
          </button>
        </div>
      </div>

      <aside class="hero-proof" data-reveal aria-label="Flujo de trabajo">
        <span class="hero-proof__rule" aria-hidden="true"></span>
        <p>inventario</p>
        <p>receta</p>
        <p>historial</p>
      </aside>
    </section>

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
              <h2>Flujo real</h2>
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
              <li><span>1</span>Crear cuenta o iniciar sesion.</li>
              <li><span>2</span>Registrar cantidades y unidades.</li>
              <li><span>3</span>Pedir una propuesta de receta al backend.</li>
              <li><span>4</span>Revisar, calificar o borrar del historial.</li>
            </ol>
          </div>
        </div>
      </template>
    </Teleport>
  </article>
</template>

<style scoped>
.welcome-root {
  position: relative;
  height: 100%;
  width: min(1240px, 100%);
  margin: 0 auto;
  overflow: hidden;
  perspective: 1200px;
}

.welcome-root::before {
  content: "";
  position: absolute;
  inset: clamp(18px, 4vw, 42px) 0 auto auto;
  width: min(44vw, 520px);
  aspect-ratio: 1;
  border-radius: 50%;
  pointer-events: none;
  background:
    radial-gradient(circle at 36% 30%, rgb(255 255 255 / 0.75), transparent 24%),
    conic-gradient(from 220deg, rgb(38 116 81 / 0.22), rgb(194 135 58 / 0.24), rgb(15 36 24 / 0.08), rgb(38 116 81 / 0.22));
  filter: blur(6px);
  opacity: 0.82;
}

.welcome-hero {
  position: relative;
  height: 100%;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(108px, 180px);
  gap: clamp(22px, 5vw, 74px);
  align-items: center;
  padding: clamp(8px, 2.8vh, 28px) 0;
  overflow: hidden;
}

.welcome-hero__main {
  display: grid;
  gap: clamp(12px, 2.4vh, 24px);
  align-content: center;
  min-width: 0;
}

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
  background: rgb(254 253 248 / 0.76);
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  box-shadow: 0 12px 30px -20px rgb(15 36 24 / 0.3);
  -webkit-backdrop-filter: blur(14px);
  backdrop-filter: blur(14px);
}

.hero-eyebrow__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-accent);
  box-shadow: 0 0 0 4px rgb(38 116 81 / 0.18);
}

.hero-title {
  margin: 0;
  display: flex;
  flex-wrap: nowrap;
  color: var(--color-ink);
  font-family: "Bricolage Grotesque", system-ui, serif;
  font-size: clamp(5.6rem, min(18vw, 23vh), 15.5rem);
  font-weight: 760;
  letter-spacing: -0.04em;
  line-height: 0.78;
  text-transform: lowercase;
  transform-style: preserve-3d;
}

.hero-letter {
  display: inline-block;
  cursor: default;
  transform-origin: 50% 80%;
  transition:
    color 320ms ease,
    font-weight 280ms var(--ease-out),
    margin 280ms var(--ease-out),
    text-shadow 320ms ease,
    transform 320ms var(--ease-out);
  user-select: none;
  will-change: transform;
}

.hero-letter:hover {
  color: var(--color-accent);
  font-weight: 820;
  margin: 0 5px;
  transform: translateY(-6px) scale(1.045);
  text-shadow: 0 14px 34px rgb(38 116 81 / 0.3);
}

.hero-subtitle {
  max-width: 58ch;
  margin: 0;
  color: var(--color-ink-soft);
  font-family: "DM Sans", system-ui;
  font-size: clamp(1rem, min(1.5vw, 2.4vh), 1.32rem);
  line-height: 1.5;
  letter-spacing: 0;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 2px;
}

.cta {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  min-height: 54px;
  padding: 0 28px;
  border-radius: var(--radius-button);
  font-family: "DM Sans", system-ui;
  font-size: 0.98rem;
  font-weight: 800;
  letter-spacing: 0;
  cursor: pointer;
  overflow: hidden;
  transition:
    transform 280ms cubic-bezier(0.34, 1.56, 0.64, 1),
    box-shadow 280ms ease;
  will-change: transform;
}

.cta::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  opacity: 0;
  transition: opacity 280ms ease;
  pointer-events: none;
}

.cta__inner {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  z-index: 1;
}

.cta--primary {
  color: var(--color-panel);
  background:
    linear-gradient(180deg, #3a8a64, var(--color-accent) 78%),
    var(--color-accent);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.18),
    0 24px 54px -16px rgb(38 116 81 / 0.56);
}

.cta--primary::before {
  background: linear-gradient(180deg, #4a9a74, #2a7a54 78%);
}

.cta--ghost {
  color: var(--color-ink);
  background: rgb(254 253 248 / 0.78);
  box-shadow:
    inset 0 0 0 1px rgb(15 36 24 / 0.1),
    0 16px 34px -20px rgb(15 36 24 / 0.2);
  -webkit-backdrop-filter: blur(14px);
  backdrop-filter: blur(14px);
}

.cta--ghost::before {
  background: rgb(255 255 255 / 0.9);
}

.cta__arrow {
  display: inline-grid;
  width: 28px;
  height: 28px;
  place-items: center;
  border-radius: 50%;
  color: inherit;
  background: rgb(255 255 255 / 0.22);
  transition: transform 280ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.cta:active {
  transform: scale(0.96);
  transition-duration: 120ms;
}

.hero-proof {
  display: grid;
  gap: clamp(10px, 1.8vh, 18px);
  justify-items: end;
  align-self: center;
  color: var(--color-ink);
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: clamp(0.74rem, 1vw, 0.86rem);
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.hero-proof p {
  margin: 0;
  writing-mode: vertical-rl;
  transform: rotate(180deg);
}

.hero-proof__rule {
  width: 1px;
  height: min(24vh, 180px);
  background: linear-gradient(180deg, transparent, var(--color-accent), transparent);
}

.flow-backdrop {
  position: fixed;
  inset: 0;
  z-index: 999;
  background:
    radial-gradient(circle at var(--blendy-backdrop-x, 50%) var(--blendy-backdrop-y, 50%), rgb(38 116 81 / 0.18), transparent 34%),
    rgb(15 36 24 / 0.36);
  -webkit-backdrop-filter: blur(16px) saturate(120%);
  backdrop-filter: blur(16px) saturate(120%);
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
  border-radius: 30px;
  background:
    linear-gradient(150deg, rgb(254 253 248 / 0.98), rgb(236 240 226 / 0.96)),
    var(--color-panel);
  box-shadow:
    0 0 0 1px rgb(255 255 255 / 0.08),
    0 48px 120px -20px rgb(15 36 24 / 0.36),
    0 20px 50px -15px rgb(38 116 81 / 0.18);
  transform-origin: var(--blendy-origin-x, 50%) var(--blendy-origin-y, 50%);
}

.flow-modal-card::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  background: radial-gradient(circle at 20% 0%, rgb(255 255 255 / 0.7), transparent 50%);
}

.flow-modal-header {
  position: relative;
  display: flex;
  gap: 18px;
  align-items: start;
  justify-content: space-between;
  padding: 28px 28px 0;
}

.flow-modal-header h2 {
  margin: 0;
  color: var(--color-ink);
  font-family: "Bricolage Grotesque", system-ui;
  font-size: clamp(2rem, 4vw, 2.6rem);
  font-weight: 760;
  line-height: 0.95;
  letter-spacing: -0.02em;
}

.flow-modal-close {
  display: grid;
  flex: 0 0 auto;
  width: 44px;
  height: 44px;
  place-items: center;
  border: 1px solid rgb(15 36 24 / 0.1);
  border-radius: 50%;
  color: var(--color-ink);
  background: var(--color-panel);
  line-height: 1;
  transition:
    background 180ms ease,
    color 180ms ease,
    transform 160ms var(--ease-out);
}

.flow-modal-close:active {
  transform: scale(0.92);
}

.modal-flow {
  position: relative;
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
  border: 1px solid rgb(15 36 24 / 0.06);
  border-radius: 18px;
  color: var(--color-ink);
  background: var(--color-soft);
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0;
}

.modal-flow span {
  display: grid;
  width: 32px;
  height: 32px;
  place-items: center;
  border-radius: 50%;
  color: var(--color-panel);
  background:
    linear-gradient(180deg, #3a8a64, var(--color-accent) 80%),
    var(--color-accent);
  font-family: "Bricolage Grotesque", system-ui;
  font-size: 0.95rem;
  font-weight: 760;
}

@media (hover: hover) and (pointer: fine) {
  .cta--primary:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / 0.2),
      0 30px 66px -16px rgb(38 116 81 / 0.62);
  }

  .cta--primary:hover::before {
    opacity: 1;
  }

  .cta--primary:hover .cta__arrow {
    transform: translateX(4px);
  }

  .cta--ghost:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow:
      inset 0 0 0 1px rgb(38 116 81 / 0.2),
      0 20px 40px -16px rgb(15 36 24 / 0.25);
  }

  .cta--ghost:hover::before {
    opacity: 1;
  }

  .flow-modal-close:hover {
    color: var(--color-accent-strong);
    background: var(--color-accent-soft);
  }
}

@media (max-width: 820px) {
  .welcome-hero {
    grid-template-columns: 1fr;
  }

  .hero-proof {
    position: absolute;
    right: 0;
    bottom: 12px;
    grid-auto-flow: column;
    align-items: center;
  }

  .hero-proof p {
    writing-mode: initial;
    transform: none;
  }

  .hero-proof__rule {
    width: 56px;
    height: 1px;
  }
}

@media (max-width: 600px) {
  .welcome-root {
    width: min(100% - 24px, 560px);
  }

  .welcome-hero {
    align-content: center;
    padding-bottom: 46px;
  }

  .hero-title {
    font-size: clamp(4.1rem, min(24vw, 18vh), 7.6rem);
  }

  .hero-actions {
    display: grid;
    grid-template-columns: 1fr;
  }

  .cta {
    width: 100%;
  }

  .hero-proof {
    left: 0;
    right: auto;
    justify-items: start;
    font-size: 0.68rem;
    letter-spacing: 0.08em;
  }
}

@media (max-height: 720px) {
  .hero-eyebrow {
    padding-block: 6px;
  }

  .hero-title {
    font-size: clamp(4.2rem, min(15vw, 20vh), 12rem);
  }

  .hero-subtitle {
    max-width: 62ch;
    font-size: 1rem;
  }

  .cta {
    min-height: 48px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .flow-backdrop {
    animation: none;
  }
}
</style>
