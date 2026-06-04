<script setup lang="ts">
import { computed, ref } from 'vue'
import AppShell from './components/AppShell.vue'
import AuthPanel from './components/AuthPanel.vue'
import InventoryPanel from './components/InventoryPanel.vue'
import { useAuthSession } from './composables/useAuthSession'
import type { Ingredient } from './types/api'

const { token, isAuthenticated, setToken, clearSession } = useAuthSession()
const activeView = ref(isAuthenticated.value ? 'inventory' : 'auth')
const ingredients = ref<Ingredient[]>([])

const heroTitle = computed(() =>
  isAuthenticated.value
    ? 'Cocina desde lo que ya tienes'
    : 'Convierte tu inventario en recetas listas para preparar',
)

function navigate(view: string) {
  activeView.value = view
}

function logout() {
  clearSession()
  ingredients.value = []
  activeView.value = 'auth'
}

function handleAuthenticated(token: string) {
  setToken(token)
  activeView.value = 'inventory'
}

function handleIngredientsUpdated(nextIngredients: Ingredient[]) {
  ingredients.value = nextIngredients
}
</script>

<template>
  <AppShell
    :active-view="activeView"
    :is-authenticated="isAuthenticated"
    @navigate="navigate"
    @logout="logout"
  >
    <main class="page">
      <section class="hero">
        <div class="hero__content">
          <p class="hero__eyebrow">Proyecto final</p>
          <h1>{{ heroTitle }}</h1>
          <p>
            Registra ingredientes, genera una receta estructurada con IA y guarda
            el historial para calificar tus mejores resultados.
          </p>
          <div class="hero__actions">
            <button class="pill-button" type="button" @click="navigate('auth')">
              Empezar
            </button>
            <button class="pill-button pill-button--light" type="button" @click="navigate('preview')">
              Ver flujo
            </button>
          </div>
        </div>
        <aside class="hero__panel" aria-label="Resumen de la aplicación">
          <span>Inventario</span>
          <strong>{{ ingredients.length }} ingredientes</strong>
          <div class="panel-line"></div>
          <span>Recetas guardadas</span>
          <strong>0 recetas</strong>
        </aside>
      </section>

      <section class="workspace">
        <AuthPanel
          v-if="activeView === 'auth' && !isAuthenticated"
          @authenticated="handleAuthenticated"
        />
        <InventoryPanel
          v-else-if="activeView === 'inventory'"
          :token="token"
          @updated="handleIngredientsUpdated"
        />
        <article v-else class="workspace__card">
          <p class="workspace__label">{{ activeView }}</p>
          <h2>Área de trabajo preparada</h2>
          <p>
            En los siguientes commits esta zona recibirá autenticación, CRUD de
            ingredientes, generación de recetas, historial y calificaciones.
          </p>
        </article>
      </section>
    </main>
  </AppShell>
</template>

<style scoped>
.page {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  padding: 40px 0 64px;
}

.hero {
  min-height: min(720px, calc(100dvh - 140px));
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, 420px);
  gap: 32px;
  align-items: end;
}

.hero__content {
  padding: 60px 0;
}

.hero__eyebrow,
.workspace__label {
  margin: 0 0 12px;
  color: var(--color-accent);
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.hero h1 {
  margin: 0;
  max-width: 860px;
  font-size: clamp(3rem, 8vw, 7.4rem);
  line-height: 0.9;
  letter-spacing: 0;
}

.hero p,
.workspace__card p {
  max-width: 58ch;
  color: var(--color-muted);
  font-size: 1.05rem;
  line-height: 1.7;
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}

.pill-button {
  min-height: 48px;
  border: 0;
  border-radius: var(--radius-button);
  padding: 0 22px;
  color: #ffffff;
  background: var(--color-accent);
  font-weight: 800;
  transition:
    transform 150ms var(--ease-out),
    background 180ms ease,
    box-shadow 180ms ease;
  box-shadow: 0 12px 30px rgb(38 116 81 / 0.22);
}

.pill-button:active {
  transform: scale(0.97);
}

.pill-button--light {
  color: var(--color-ink);
  background: #ffffff;
  box-shadow: inset 0 0 0 1px var(--color-line);
}

.hero__panel,
.workspace__card {
  border: 1px solid rgb(18 35 26 / 0.08);
  border-radius: var(--radius-card);
  background: rgb(255 255 255 / 0.82);
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(18px);
}

.hero__panel {
  display: grid;
  gap: 10px;
  padding: 28px;
}

.hero__panel span {
  color: var(--color-muted);
  font-size: 0.95rem;
}

.hero__panel strong {
  font-size: 2rem;
  line-height: 1;
}

.panel-line {
  height: 1px;
  margin: 10px 0;
  background: var(--color-line);
}

.workspace {
  padding-top: 20px;
}

.workspace__card {
  padding: 28px;
}

.workspace__card h2 {
  margin: 0;
  font-size: clamp(1.8rem, 4vw, 3rem);
  line-height: 1;
}

@media (hover: hover) and (pointer: fine) {
  .pill-button:hover {
    transform: translateY(-1px);
    background: var(--color-accent-strong);
  }

  .pill-button--light:hover {
    color: var(--color-accent-strong);
    background: #ffffff;
  }
}

@media (max-width: 820px) {
  .page {
    width: min(100% - 24px, 680px);
    padding-top: 24px;
  }

  .hero {
    min-height: auto;
    grid-template-columns: 1fr;
  }

  .hero__content {
    padding: 36px 0 0;
  }

  .hero h1 {
    font-size: clamp(2.7rem, 16vw, 5rem);
  }
}
</style>
