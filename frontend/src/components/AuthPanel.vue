<script setup lang="ts">
import { computed, ref } from 'vue'

const emit = defineEmits<{
  authenticated: [token: string]
}>()

type AuthMode = 'login' | 'register'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

const mode = ref<AuthMode>('login')
const name = ref('')
const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const isRegister = computed(() => mode.value === 'register')
const title = computed(() =>
  isRegister.value ? 'Crear cuenta' : 'Entrar al inventario',
)
const helper = computed(() =>
  isRegister.value
    ? 'Registra tu usuario para guardar ingredientes y recetas.'
    : 'Inicia sesión para continuar con tu inventario personal.',
)
const submitLabel = computed(() =>
  isLoading.value
    ? 'Procesando'
    : isRegister.value
      ? 'Crear cuenta'
      : 'Entrar',
)

function setMode(nextMode: AuthMode) {
  mode.value = nextMode
  errorMessage.value = ''
  successMessage.value = ''
}

function validateForm() {
  if (isRegister.value && name.value.trim().length < 2) {
    return 'El nombre debe tener al menos 2 caracteres.'
  }

  if (!email.value.includes('@') || email.value.trim().length < 5) {
    return 'Escribe un correo válido.'
  }

  if (password.value.length < 6) {
    return 'La contraseña debe tener al menos 6 caracteres.'
  }

  return ''
}

async function submitForm() {
  const validationError = validateForm()

  if (validationError) {
    errorMessage.value = validationError
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const endpoint = isRegister.value ? '/auth/register' : '/auth/login'
    const payload = isRegister.value
      ? {
          nombre: name.value.trim(),
          email: email.value.trim(),
          password: password.value,
        }
      : {
          email: email.value.trim(),
          password: password.value,
        }

    const response = await fetch(`${apiBaseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    const data = await response.json().catch(() => null)

    if (!response.ok) {
      const detail = data && typeof data.detail === 'string' ? data.detail : ''
      throw new Error(detail || 'No se pudo completar la solicitud.')
    }

    if (isRegister.value) {
      successMessage.value = 'Cuenta creada. Ahora puedes iniciar sesión.'
      mode.value = 'login'
      password.value = ''
      return
    }

    const token = data && typeof data.access_token === 'string' ? data.access_token : ''

    if (!token) {
      throw new Error('La API no devolvió un token válido.')
    }

    emit('authenticated', token)
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Ocurrió un error inesperado.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <article class="auth-panel" aria-labelledby="auth-title">
    <div class="auth-panel__copy">
      <p class="workspace__label">Acceso</p>
      <h2 id="auth-title">{{ title }}</h2>
      <p>{{ helper }}</p>
    </div>

    <div class="auth-tabs" role="tablist" aria-label="Modo de acceso">
      <button
        class="auth-tabs__button"
        :class="{ 'auth-tabs__button--active': mode === 'login' }"
        type="button"
        @click="setMode('login')"
      >
        Iniciar sesión
      </button>
      <button
        class="auth-tabs__button"
        :class="{ 'auth-tabs__button--active': mode === 'register' }"
        type="button"
        @click="setMode('register')"
      >
        Registro
      </button>
    </div>

    <form class="auth-form" @submit.prevent="submitForm">
      <label v-if="isRegister">
        <span>Nombre</span>
        <input v-model="name" autocomplete="name" name="name" placeholder="Ángel" />
      </label>

      <label>
        <span>Correo</span>
        <input
          v-model="email"
          autocomplete="email"
          name="email"
          placeholder="angel@email.com"
          type="email"
        />
      </label>

      <label>
        <span>Contraseña</span>
        <input
          v-model="password"
          :autocomplete="isRegister ? 'new-password' : 'current-password'"
          name="password"
          placeholder="Mínimo 6 caracteres"
          type="password"
        />
      </label>

      <p v-if="errorMessage" class="form-message form-message--error">
        {{ errorMessage }}
      </p>
      <p v-if="successMessage" class="form-message form-message--success">
        {{ successMessage }}
      </p>

      <button class="pill-button auth-form__submit" :disabled="isLoading" type="submit">
        {{ submitLabel }}
      </button>
    </form>
  </article>
</template>
