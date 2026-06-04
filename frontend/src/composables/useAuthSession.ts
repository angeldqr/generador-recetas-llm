import { computed, ref } from 'vue'

const TOKEN_STORAGE_KEY = 'recetas_llm_token'

const token = ref(localStorage.getItem(TOKEN_STORAGE_KEY) ?? '')

interface SessionPayload {
  sub?: string
  email?: string
  nombre?: string
  name?: string
  exp?: number
  iat?: number
  [key: string]: unknown
}

function decodeJwtPayload(value: string): SessionPayload | null {
  const [, payload] = value.split('.')
  if (!payload) return null

  try {
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/')
    const padded = normalized.padEnd(
      normalized.length + ((4 - (normalized.length % 4)) % 4),
      '=',
    )
    const binary = window.atob(padded)
    const bytes = Uint8Array.from(binary, (char) => char.charCodeAt(0))
    return JSON.parse(new TextDecoder().decode(bytes)) as SessionPayload
  } catch {
    return null
  }
}

export function useAuthSession() {
  const isAuthenticated = computed(() => Boolean(token.value))
  const sessionPayload = computed(() => decodeJwtPayload(token.value))

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
    sessionPayload,
    setToken,
    clearSession,
  }
}
