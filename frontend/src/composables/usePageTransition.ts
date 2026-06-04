import gsap from 'gsap'
import { onBeforeUnmount, ref, type Ref } from 'vue'
import { useRoute } from 'vue-router'

function shouldReduceMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

/**
 * Composable that applies a soft, interruptible page enter animation
 * to a ref of the page root element whenever the route changes.
 * Honors prefers-reduced-motion.
 */
export function usePageTransition(target: Ref<HTMLElement | null>) {
  const isReady = ref(false)
  const route = useRoute()
  let enterTween: gsap.core.Tween | null = null

  function playEnter() {
    if (!target.value) return
    if (enterTween) {
      enterTween.kill()
      enterTween = null
    }

    if (shouldReduceMotion()) {
      gsap.set(target.value, { autoAlpha: 1, y: 0, filter: 'blur(0px)' })
      isReady.value = true
      return
    }

    enterTween = gsap.fromTo(
      target.value,
      {
        autoAlpha: 0,
        y: 14,
        filter: 'blur(2px)',
      },
      {
        autoAlpha: 1,
        y: 0,
        filter: 'blur(0px)',
        duration: 0.36,
        ease: 'power3.out',
        clearProps: 'filter',
        onStart: () => {
          isReady.value = false
        },
        onComplete: () => {
          isReady.value = true
        },
      },
    )
  }

  function staggerIn(selector: string, options: gsap.TweenVars = {}) {
    if (!target.value) return
    const elements = target.value.querySelectorAll<HTMLElement>(selector)
    if (!elements.length) return

    if (shouldReduceMotion()) {
      gsap.set(elements, { autoAlpha: 1, y: 0 })
      return
    }

    gsap.fromTo(
      elements,
      { autoAlpha: 0, y: 16 },
      {
        autoAlpha: 1,
        y: 0,
        duration: 0.45,
        ease: 'power3.out',
        stagger: 0.06,
        ...options,
      },
    )
  }

  // Play on first mount and every route change.
  if (target.value) {
    playEnter()
  }

  // Re-play when the route name changes (and on first paint).
  // Using watchEffect would be cleaner, but we want a single trigger.
  // The composable consumers will re-invoke playEnter() on their onMounted.
  // We just expose a cleanup hook.
  onBeforeUnmount(() => {
    if (enterTween) enterTween.kill()
  })

  return {
    playEnter,
    staggerIn,
    isReady,
    route,
  }
}
