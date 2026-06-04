<script setup lang="ts">
import { computed, ref } from 'vue'
import { loginUser, registerUser } from '../services/api'

const emit = defineEmits<{
  authenticated: [token: string]
}>()

type AuthMode = 'login' | 'register'

const mode = ref<AuthMode>('login')
const name = ref('')
const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const isRegister = computed(() => mode.value === 'register')
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
    return 'Escribe un correo valido.'
  }

  if (password.value.length < 6) {
    return 'La contrasena debe tener al menos 6 caracteres.'
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
    if (isRegister.value) {
      await registerUser({
        nombre: name.value.trim(),
        email: email.value.trim(),
        password: password.value,
      })
      successMessage.value = 'Cuenta creada. Ahora puedes iniciar sesion.'
      mode.value = 'login'
      password.value = ''
      return
    }

    const data = await loginUser({
      email: email.value.trim(),
      password: password.value,
    })

    emit('authenticated', data.access_token)
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Ocurrio un error inesperado.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <article class="auth-panel" aria-label="Formulario de acceso">
    <div class="auth-tabs" role="tablist" aria-label="Modo de acceso">
      <button
        class="auth-tabs__button"
        :class="{ 'auth-tabs__button--active': mode === 'login' }"
        type="button"
        @click="setMode('login')"
      >
        Iniciar sesion
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
        <input v-model="name" autocomplete="name" name="name" placeholder="Tu nombre" />
      </label>

      <label>
        <span>Correo</span>
        <input
          v-model="email"
          autocomplete="email"
          name="email"
          placeholder="tu@correo.com"
          type="email"
        />
      </label>

      <label>
        <span>Contrasena</span>
        <input
          v-model="password"
          :autocomplete="isRegister ? 'new-password' : 'current-password'"
          name="password"
          placeholder="Minimo 6 caracteres"
          type="password"
        />
      </label>

      <p v-if="errorMessage" class="form-message form-message--error" role="alert">
        {{ errorMessage }}
      </p>
      <p v-if="successMessage" class="form-message form-message--success" role="status">
        {{ successMessage }}
      </p>

      <button class="auth-form__submit" :disabled="isLoading" type="submit">
        {{ submitLabel }}
      </button>
    </form>
  </article>
</template>
