import { computed, ref } from 'vue'

const TOKEN_STORAGE_KEY = 'recetas_llm_token'

const token = ref(localStorage.getItem(TOKEN_STORAGE_KEY) ?? '')

export function useAuthSession() {
  const isAuthenticated = computed(() => Boolean(token.value))

  function setToken(nextToken: string) {
    token.value = nextToken
    localStorage.setItem(TOKEN_STORAGE_KEY, nextToken)
  }

  function clearSession() {
    token.value = ''
    localStorage.removeItem(TOKEN_STORAGE_KEY)
  }

  return {
    token,
    isAuthenticated,
    setToken,
    clearSession,
  }
}
