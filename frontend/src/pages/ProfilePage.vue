<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '../components/BaseButton.vue'
import BaseCard from '../components/BaseCard.vue'
import { useAuthSession } from '../composables/useAuthSession'

const { token, isAuthenticated, sessionPayload, clearSession } = useAuthSession()
const router = useRouter()

const sessionLabel = computed(() =>
  isAuthenticated.value ? 'Sesion activa' : 'Sesion inactiva',
)

const displayName = computed(() => {
  const payload = sessionPayload.value
  const value = payload?.nombre ?? payload?.name
  return typeof value === 'string' && value.trim() ? value : 'No disponible'
})

const displayEmail = computed(() => {
  const payload = sessionPayload.value
  const sub = typeof payload?.sub === 'string' ? payload.sub : ''
  const email = typeof payload?.email === 'string' ? payload.email : ''
  if (email.includes('@')) return email
  if (sub.includes('@')) return sub
  return 'No disponible'
})

const tokenPreview = computed(() => {
  if (!token.value) return 'Sin token local'
  return `${token.value.slice(0, 10)}...${token.value.slice(-6)}`
})

const expiryLabel = computed(() => {
  const exp = sessionPayload.value?.exp
  if (typeof exp !== 'number') return 'No informado'

  return new Intl.DateTimeFormat('es-CO', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(exp * 1000))
})

function handleLogout() {
  clearSession()
  void router.push({ name: 'welcome' })
}
</script>

<template>
  <article class="page page--profile" data-route="profile">
    <BaseCard class="profile-card">
      <div class="profile-card__topline">
        <p class="profile-card__eyebrow">Perfil</p>
        <span class="profile-card__status">{{ sessionLabel }}</span>
      </div>

      <h1 class="profile-card__title">Cuenta local</h1>
      <p class="profile-card__hint">
        Esta pantalla muestra solo lo que la sesion actual expone en el navegador.
      </p>

      <dl class="profile-card__list">
        <div>
          <dt>Nombre</dt>
          <dd>{{ displayName }}</dd>
        </div>
        <div>
          <dt>Correo</dt>
          <dd>{{ displayEmail }}</dd>
        </div>
        <div>
          <dt>Expira</dt>
          <dd>{{ expiryLabel }}</dd>
        </div>
        <div>
          <dt>Token</dt>
          <dd class="profile-card__token">{{ tokenPreview }}</dd>
        </div>
      </dl>

      <BaseButton
        class="profile-card__logout"
        type="button"
        :disabled="!isAuthenticated"
        @click="handleLogout"
      >
        Cerrar sesion
      </BaseButton>
    </BaseCard>
  </article>
</template>

<style scoped>
.page--profile {
  width: min(760px, 100%);
  margin: 0 auto;
  padding-top: 32px;
}

.profile-card {
  position: relative;
  display: grid;
  gap: 18px;
  overflow: hidden;
  padding: 36px;
}

.profile-card::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 100% 0%, rgb(38 116 81 / 0.14), transparent 34%),
    linear-gradient(90deg, rgb(15 36 24 / 0.05), transparent 26%);
}

.profile-card > * {
  position: relative;
}

.profile-card__topline {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
}

.profile-card__eyebrow,
.profile-card__status {
  margin: 0;
  font-family: "JetBrains Mono", monospace;
  font-size: 0.74rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.profile-card__eyebrow {
  color: var(--color-accent);
}

.profile-card__status {
  border-radius: var(--radius-button);
  padding: 7px 12px;
  color: var(--color-accent-strong);
  background: var(--color-accent-soft);
}

.profile-card__title {
  margin: 0;
  color: var(--color-ink);
  font-family: "Bricolage Grotesque", system-ui;
  font-size: clamp(2.4rem, 5vw, 3.6rem);
  font-weight: 760;
  line-height: 0.95;
  letter-spacing: -0.03em;
}

.profile-card__hint {
  max-width: 60ch;
  margin: 0;
  color: var(--color-muted);
  font-family: "DM Sans", system-ui;
  line-height: 1.55;
}

.profile-card__list {
  display: grid;
  margin: 8px 0 0;
  padding: 0;
}

.profile-card__list > div {
  display: grid;
  grid-template-columns: 160px minmax(0, 1fr);
  gap: 16px;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid var(--color-line);
}

.profile-card__list > div:last-child {
  border-bottom: 0;
}

.profile-card__list dt {
  color: var(--color-muted);
  font-family: "JetBrains Mono", monospace;
  font-size: 0.74rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.profile-card__list dd {
  min-width: 0;
  margin: 0;
  color: var(--color-ink);
  font-family: "DM Sans", system-ui;
  font-weight: 800;
  overflow-wrap: anywhere;
}

.profile-card__token {
  color: var(--color-accent-strong);
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 0.9rem;
}

.profile-card__logout {
  justify-self: start;
  margin-top: 10px;
}

@media (max-width: 600px) {
  .profile-card {
    padding: 24px;
  }

  .profile-card__topline {
    align-items: start;
    flex-direction: column;
  }

  .profile-card__list > div {
    grid-template-columns: 1fr;
    gap: 5px;
  }

  .profile-card__logout {
    width: 100%;
  }
}
</style>
