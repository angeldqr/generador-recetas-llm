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
    ? 'Tu sesion esta protegida con un token de acceso. Puedes cerrarla cuando quieras.'
    : 'Inicia sesion para acceder a tu inventario y a tus recetas guardadas.',
)

function handleLogout() {
  clearSession()
  void router.push({ name: 'welcome' })
}
</script>

<template>
  <article class="page page--profile" data-route="profile">
    <section class="profile-card">
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
        class="profile-card__logout"
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
  padding-top: 32px;
}

.profile-card {
  border: 1px solid rgb(15 36 24 / 0.08);
  border-radius: 32px;
  padding: 36px;
  background:
    linear-gradient(160deg, rgb(254 253 248 / 0.96), rgb(244 241 232 / 0.92)),
    var(--color-panel);
  box-shadow: var(--shadow-card);
  display: grid;
  gap: 18px;
}

.profile-card__eyebrow {
  margin: 0;
  color: var(--color-accent);
  font-family: "JetBrains Mono", monospace;
  font-size: 0.74rem;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.profile-card__title {
  margin: 0;
  font-family: "Bricolage Grotesque", system-ui;
  font-size: clamp(2.4rem, 5vw, 3.4rem);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.03em;
  color: var(--color-ink);
}

.profile-card__hint {
  margin: 0;
  color: var(--color-muted);
  font-family: "DM Sans", system-ui;
  line-height: 1.55;
  max-width: 60ch;
}

.profile-card__list {
  display: grid;
  gap: 0;
  margin: 4px 0 0;
  padding: 0;
}

.profile-card__list > div {
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: 16px;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid var(--color-line);
}

.profile-card__list > div:last-child {
  border-bottom: 0;
}

.profile-card__list dt {
  color: var(--color-muted);
  font-family: "JetBrains Mono", monospace;
  font-size: 0.74rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.profile-card__list dd {
  margin: 0;
  color: var(--color-ink);
  font-family: "DM Sans", system-ui;
  font-weight: 600;
}

.profile-card__token {
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 0.9rem;
  color: var(--color-accent-strong);
}

.profile-card__logout {
  justify-self: start;
  margin-top: 12px;
  min-height: 50px;
  padding: 0 24px;
  border: 0;
  border-radius: var(--radius-button);
  color: var(--color-panel);
  background:
    linear-gradient(180deg, #3a8a64, var(--color-accent) 78%),
    var(--color-accent);
  font-family: "DM Sans", system-ui;
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: -0.01em;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.18),
    0 18px 40px -12px rgb(38 116 81 / 0.55);
  transition:
    transform 180ms var(--ease-out),
    box-shadow 180ms ease;
}

.profile-card__logout:active {
  transform: scale(0.97);
}

@media (hover: hover) and (pointer: fine) {
  .profile-card__logout:hover {
    transform: translateY(-1px);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / 0.2),
      0 24px 50px -12px rgb(38 116 81 / 0.6);
  }
}

@media (max-width: 600px) {
  .profile-card {
    padding: 24px;
  }

  .profile-card__list > div {
    grid-template-columns: 1fr;
    gap: 4px;
  }
}
</style>
