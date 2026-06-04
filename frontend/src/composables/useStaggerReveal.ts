import gsap from 'gsap'
import { nextTick, onMounted, type Ref } from 'vue'

interface StaggerRevealOptions {
  selector: string
  root?: Ref<HTMLElement | null> | HTMLElement | null
  stagger?: number
  delay?: number
  duration?: number
  y?: number
}

function shouldReduceMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function resolveRoot(root: StaggerRevealOptions['root']): HTMLElement | null {
  if (!root) return null
  if (typeof HTMLElement !== 'undefined' && root instanceof HTMLElement) {
    return root
  }
  if (typeof root === 'object' && 'value' in root) {
    return root.value
  }
  return null
}

/**
 * Stagger-reveals the children matching `selector` inside `root` once the page has mounted.
 * Plays nicely with the GSAP-driven page transition in App.vue: we let the page
 * finish entering before we animate the inner list.
 *
 * Honors prefers-reduced-motion.
 */
export function useStaggerReveal(options: StaggerRevealOptions) {
  onMounted(async () => {
    await nextTick()
    const rootEl = resolveRoot(options.root) ?? document
    const elements = rootEl.querySelectorAll<HTMLElement>(options.selector)
    if (!elements.length) return

    if (shouldReduceMotion()) {
      gsap.set(elements, { autoAlpha: 1, y: 0 })
      return
    }

    const wait = (options.delay ?? 0.18) * 1000
    const duration = options.duration ?? 0.45
    const stagger = options.stagger ?? 0.06
    const y = options.y ?? 16

    gsap.fromTo(
      elements,
      { autoAlpha: 0, y },
      {
        autoAlpha: 1,
        y: 0,
        duration,
        ease: 'power3.out',
        stagger,
        delay: wait / 1000,
      },
    )
  })
}
