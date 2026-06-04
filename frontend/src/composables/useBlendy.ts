import { createBlendy, type Blendy } from 'blendy'

let instance: Blendy | null = null

export function useBlendy(): Blendy {
  if (!instance) {
    instance = createBlendy({ animation: 'spring' })
  }
  return instance
}
