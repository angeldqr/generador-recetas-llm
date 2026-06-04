import gsap from 'gsap'
import { nextTick, onMounted, type Ref } from 'vue'

interface HeroRevealOptions {
  root?: Ref<HTMLElement | null> | HTMLElement | null
  titleSelector?: string
  bodySelector?: string
  actionSelector?: string
  panelSelector?: string
  delay?: number
}

function shouldReduceMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function resolveRoot(root: HeroRevealOptions['root']): HTMLElement | null {
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
 * Runs a soft, editorial hero reveal: title glides in first, then body,
 * actions, and finally the side panel. Each piece uses opacity + y + blur.
 * Honors prefers-reduced-motion.
 */
export function useHeroReveal(options: HeroRevealOptions = {}) {
  const {
    titleSelector = '.welcome-hero__title',
    bodySelector = '.welcome-hero__body',
    actionSelector = '.welcome-hero__actions',
    panelSelector = '.welcome-hero__panel',
    delay = 0.1,
  } = options

  onMounted(async () => {
    await nextTick()
    const rootEl = resolveRoot(options.root) ?? document
    const title = rootEl.querySelector<HTMLElement>(titleSelector)
    const body = rootEl.querySelector<HTMLElement>(bodySelector)
    const actions = rootEl.querySelector<HTMLElement>(actionSelector)
    const panel = rootEl.querySelector<HTMLElement>(panelSelector)

    const targets = [title, body, actions, panel].filter(
      (el): el is HTMLElement => Boolean(el),
    )
    if (!targets.length) return

    if (shouldReduceMotion()) {
      gsap.set(targets, { autoAlpha: 1, y: 0, filter: 'blur(0px)' })
      return
    }

    const timeline = gsap.timeline({ delay })
    timeline.fromTo(
      title ?? targets[0],
      { autoAlpha: 0, y: 28, filter: 'blur(3px)' },
      {
        autoAlpha: 1,
        y: 0,
        filter: 'blur(0px)',
        duration: 0.7,
        ease: 'power3.out',
      },
    )

    if (body) {
      timeline.fromTo(
        body,
        { autoAlpha: 0, y: 16 },
        { autoAlpha: 1, y: 0, duration: 0.5, ease: 'power3.out' },
        '-=0.45',
      )
    }

    if (actions) {
      timeline.fromTo(
        actions,
        { autoAlpha: 0, y: 12 },
        { autoAlpha: 1, y: 0, duration: 0.4, ease: 'power3.out' },
        '-=0.35',
      )
    }

    if (panel) {
      timeline.fromTo(
        panel,
        { autoAlpha: 0, y: 24, scale: 0.96 },
        {
          autoAlpha: 1,
          y: 0,
          scale: 1,
          duration: 0.6,
          ease: 'power3.out',
        },
        '-=0.45',
      )
    }
  })
}
