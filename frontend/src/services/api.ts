import type {
  AuthToken,
  ApiMessage,
  Ingredient,
  IngredientPayload,
  IngredientUpdatePayload,
  LoginPayload,
  Recipe,
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

export function getIngredients(token: string) {
  return apiRequest<Ingredient[]>('/ingredients/', { token })
}

export function createIngredient(payload: IngredientPayload, token: string) {
  return apiRequest<Ingredient>('/ingredients/', {
    method: 'POST',
    token,
    body: JSON.stringify(payload),
  })
}

export function updateIngredient(
  ingredientId: number,
  payload: IngredientUpdatePayload,
  token: string,
) {
  return apiRequest<Ingredient>(`/ingredients/${ingredientId}`, {
    method: 'PUT',
    token,
    body: JSON.stringify(payload),
  })
}

export function deleteIngredient(ingredientId: number, token: string) {
  return apiRequest<ApiMessage>(`/ingredients/${ingredientId}`, {
    method: 'DELETE',
    token,
  })
}

export function generateRecipe(token: string) {
  return apiRequest<Recipe>('/recipes/generate', {
    method: 'POST',
    token,
  })
}
