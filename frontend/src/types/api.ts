export interface AuthToken {
  access_token: string
  token_type: string
}

export interface RegisterPayload {
  nombre: string
  email: string
  password: string
}

export interface LoginPayload {
  email: string
  password: string
}

export interface UserResponse {
  id: number
  nombre: string
  email: string
}

export interface Ingredient {
  id: number
  nombre: string
  cantidad: number
  unidad: string
}

export interface IngredientPayload {
  nombre: string
  cantidad: number
  unidad: string
}

export type IngredientUpdatePayload = Partial<IngredientPayload>

export interface ApiMessage {
  message: string
}
