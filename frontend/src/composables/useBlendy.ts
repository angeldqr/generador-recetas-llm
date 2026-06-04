import { createBlendy, type Blendy } from 'blendy'

let instance: Blendy | null = null

export function useBlendy(): Blendy {
  if (!instance) {
    // Use spring animation but configure it for smoother performance
    instance = createBlendy({
      animation: 'spring',
    })
  }
  return instance
}
