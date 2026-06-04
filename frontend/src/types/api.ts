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
