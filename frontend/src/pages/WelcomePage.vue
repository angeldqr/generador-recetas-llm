<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseModal from '../components/BaseModal.vue'
import { useAppData } from '../composables/useAppData'
import { useAuthSession } from '../composables/useAuthSession'
import { useHeroReveal } from '../composables/useHeroReveal'

const { ingredients, recipes } = useAppData()
const { isAuthenticated } = useAuthSession()
const router = useRouter()
const isFlowModalOpen = ref(false)

useHeroReveal()

const heroEyebrow = 'Proyecto final'
const heroTitle = computed(() =>
  isAuthenticated.value
    ? 'Cocina desde lo que ya tienes'
    : 'Convierte tu inventario en recetas listas para preparar',
)
const heroBody =
  'Registra ingredientes, genera una receta estructurada con IA y guarda el historial para calificar tus mejores resultados.'

const primaryLabel = computed(() =>
  isAuthenticated.value ? 'Ir al inventario' : 'Empezar',
)
const secondaryLabel = 'Ver flujo'

function goToPrimary() {
  if (isAuthenticated.value) {
    void router.push({ name: 'inventory' })
    return
  }
  void router.push({ name: 'auth' })
}

function openFlowModal() {
  isFlowModalOpen.value = true
}
</script>

<template>
  <article class="page page--welcome" data-route="welcome">
    <section class="welcome-hero">
      <div class="welcome-hero__content">
        <p class="welcome-hero__eyebrow">{{ heroEyebrow }}</p>
        <h1 class="welcome-hero__title">{{ heroTitle }}</h1>
        <p class="welcome-hero__body">{{ heroBody }}</p>
        <div class="welcome-hero__actions">
          <button class="pill-button" type="button" @click="goToPrimary">
            {{ primaryLabel }}
          </button>
          <button
            class="pill-button pill-button--light"
            data-blendy-from="flow-modal"
            type="button"
            @click="openFlowModal"
          >
            <span>{{ secondaryLabel }}</span>
          </button>
        </div>
      </div>
      <aside class="welcome-hero__panel" aria-label="Resumen de la aplicación">
        <span>Inventario</span>
        <strong>{{ ingredients.length }} ingredientes</strong>
        <div class="panel-line"></div>
        <span>Recetas guardadas</span>
        <strong>{{ recipes.length }} recetas</strong>
      </aside>
    </section>

    <BaseModal
      blendy-id="flow-modal"
      :open="isFlowModalOpen"
      title="Flujo de uso"
      @close="isFlowModalOpen = false"
    >
      <ol class="modal-flow">
        <li><span>1</span>Crear cuenta o iniciar sesión</li>
        <li><span>2</span>Registrar ingredientes disponibles</li>
        <li><span>3</span>Generar receta estructurada con IA</li>
        <li><span>4</span>Guardar, calificar o eliminar del historial</li>
      </ol>
    </BaseModal>
  </article>
</template>

<style scoped>
.page--welcome {
  width: min(1180px, 100%);
  margin: 0 auto;
}

.welcome-hero {
  min-height: min(720px, calc(100dvh - 140px));
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, 420px);
  gap: 32px;
  align-items: end;
}

.welcome-hero__content {
  padding: 60px 0;
}

.welcome-hero__eyebrow {
  margin: 0 0 12px;
  color: var(--color-accent);
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.welcome-hero__title {
  margin: 0;
  max-width: 860px;
  font-size: clamp(3rem, 8vw, 7.4rem);
  line-height: 0.9;
  letter-spacing: 0;
}

.welcome-hero__body {
  max-width: 58ch;
  color: var(--color-muted);
  font-size: 1.05rem;
  line-height: 1.7;
}

.welcome-hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}

.welcome-hero__panel {
  display: grid;
  gap: 10px;
  padding: 28px;
  border: 1px solid rgb(18 35 26 / 0.08);
  border-radius: var(--radius-card);
  background: rgb(255 255 255 / 0.82);
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

.welcome-hero__panel span {
  color: var(--color-muted);
  font-size: 0.95rem;
}

.welcome-hero__panel strong {
  font-size: 2rem;
  line-height: 1;
}

.panel-line {
  height: 1px;
  margin: 10px 0;
  background: var(--color-line);
}

@media (max-width: 820px) {
  .welcome-hero {
    min-height: auto;
    grid-template-columns: 1fr;
  }

  .welcome-hero__content {
    padding: 36px 0 0;
  }

  .welcome-hero__title {
    font-size: clamp(2.7rem, 16vw, 5rem);
  }
}
</style>
