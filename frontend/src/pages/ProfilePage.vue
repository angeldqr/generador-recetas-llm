<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthSession } from '../composables/useAuthSession'

const { token, isAuthenticated, clearSession } = useAuthSession()
const router = useRouter()

const sessionLabel = computed(() =>
  isAuthenticated.value ? 'Sesion activa' : 'Sesion inactiva',
)

const sessionHint = computed(() =>
  isAuthenticated.value
    ? 'Tu sesion esta protegida con un token de acceso. Puedes cerrar sesion cuando quieras.'
    : 'Inicia sesion para acceder a tu inventario y a tus recetas guardadas.',
)

function handleLogout() {
  clearSession()
  void router.push({ name: 'welcome' })
}
</script>

<template>
  <article class="page page--profile" data-route="profile">
    <section class="profile-card" data-blendy-to="profile">
      <p class="profile-card__eyebrow">Perfil</p>
      <h1 class="profile-card__title">Tu cuenta</h1>
      <p class="profile-card__hint">{{ sessionHint }}</p>

      <dl class="profile-card__list">
        <div>
          <dt>Estado</dt>
          <dd>{{ sessionLabel }}</dd>
        </div>
        <div>
          <dt>Token</dt>
          <dd class="profile-card__token">
            <span v-if="token">{{ token.slice(0, 12) }}…</span>
            <span v-else>—</span>
          </dd>
        </div>
        <div>
          <dt>Almacenamiento</dt>
          <dd>Local (recetas_llm_token)</dd>
        </div>
      </dl>

      <button
        class="pill-button profile-card__logout"
        type="button"
        :disabled="!isAuthenticated"
        @click="handleLogout"
      >
        Cerrar sesion
      </button>
    </section>
  </article>
</template>

<style scoped>
.page--profile {
  width: min(720px, 100%);
  margin: 0 auto;
  padding-top: 12px;
}

.profile-card {
  border: 1px solid rgb(18 35 26 / 0.08);
  border-radius: var(--radius-card);
  padding: 32px;
  background:
    linear-gradient(160deg, rgb(255 255 255 / 0.94), rgb(246 247 242 / 0.9)),
    #ffffff;
  box-shadow: var(--shadow-soft);
  display: grid;
  gap: 18px;
  transform-origin: top center;
}

.profile-card__eyebrow {
  margin: 0;
  color: var(--color-accent);
  font-size: 0.82rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.profile-card__title {
  margin: 0;
  font-size: clamp(2.4rem, 5vw, 4rem);
  line-height: 0.95;
}

.profile-card__hint {
  margin: 0;
  color: var(--color-muted);
  line-height: 1.6;
  max-width: 60ch;
}

.profile-card__list {
  display: grid;
  gap: 12px;
  margin: 4px 0 0;
  padding: 0;
  border-top: 1px solid var(--color-line);
}

.profile-card__list > div {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 16px;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-line);
}

.profile-card__list dt {
  color: var(--color-muted);
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.profile-card__list dd {
  margin: 0;
  color: var(--color-ink);
  font-weight: 800;
}

.profile-card__token {
  font-family:
    ui-monospace,
    SFMono-Regular,
    Menlo,
    Consolas,
    monospace;
  font-size: 0.92rem;
  letter-spacing: 0.02em;
  color: var(--color-accent-strong);
}

.profile-card__logout {
  justify-self: start;
  margin-top: 8px;
}

@media (max-width: 600px) {
  .profile-card {
    padding: 22px;
  }

  .profile-card__list > div {
    grid-template-columns: 1fr;
    gap: 4px;
  }
}
</style>
