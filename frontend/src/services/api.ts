import type {
  AuthToken,
  LoginPayload,
  RegisterPayload,
  UserResponse,
} from '../types/api'

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'
).replace(/\/$/, '')

interface RequestOptions extends RequestInit {
  token?: string
}

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

function getErrorMessage(payload: unknown) {
  if (
    payload &&
    typeof payload === 'object' &&
    'detail' in payload &&
    typeof payload.detail === 'string'
  ) {
    return payload.detail
  }

  return 'No se pudo completar la solicitud.'
}

export async function apiRequest<T>(
  path: string,
  { token, headers, ...options }: RequestOptions = {},
) {
  const requestHeaders = new Headers(headers)

  if (!requestHeaders.has('Content-Type') && options.body) {
    requestHeaders.set('Content-Type', 'application/json')
  }

  if (token) {
    requestHeaders.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: requestHeaders,
  })

  const text = await response.text()
  const payload = text ? JSON.parse(text) : null

  if (!response.ok) {
    throw new ApiError(getErrorMessage(payload), response.status)
  }

  return payload as T
}

export function registerUser(payload: RegisterPayload) {
  return apiRequest<UserResponse>('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function loginUser(payload: LoginPayload) {
  return apiRequest<AuthToken>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
