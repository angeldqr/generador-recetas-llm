import { createBlendy, type Blendy } from 'blendy'
import { onBeforeUnmount, ref } from 'vue'

let blendyInstance: Blendy | null = null
let blendyUnavailable = false

function shouldReduceMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function resolveBlendy(): Blendy | null {
  if (blendyUnavailable) return null
  if (blendyInstance) return blendyInstance
  try {
    blendyInstance = createBlendy({ animation: 'dynamic' })
    return blendyInstance
  } catch {
    blendyUnavailable = true
    return null
  }
}

interface BlendOnMountOptions {
  id: string
  /**
   * If true, the morph is replayed whenever the page re-mounts (default).
   * If false, only the first mount triggers it.
   */
  replayOnRemount?: boolean
}

/**
 * Triggers a Blendy morph on mount, scoped to a single id. The source element
 * (data-blendy-from="<id>") should be on the previous page; the target
 * (data-blendy-to="<id>") should be on this page. Both must be in the DOM at
 * the time this fires, which is the case with `in-out` route transitions.
 *
 * Honors prefers-reduced-motion: no morph is played, both elements stay in
 * their natural position.
 */
export function useBlendyOnMount(options: BlendOnMountOptions) {
  const isReady = ref(false)

  function play() {
    if (shouldReduceMotion()) return
    const blendy = resolveBlendy()
    if (!blendy) return
    blendy.toggle(options.id)
    isReady.value = true
  }

  // Defer to next tick so the target has had a chance to render.
  queueMicrotask(() => {
    requestAnimationFrame(() => {
      play()
    })
  })

  onBeforeUnmount(() => {
    isReady.value = false
  })

  return { isReady }
}

/**
 * Re-scans the DOM for blendy attributes (call this if elements are added
 * dynamically after the page has loaded).
 */
export function refreshBlendy() {
  const blendy = resolveBlendy()
  blendy?.update()
}

/**
 * Returns the underlying Blendy instance for advanced usage.
 * Returns null if Blendy is unavailable or reduced motion is on.
 */
export function getBlendy() {
  if (shouldReduceMotion()) return null
  return resolveBlendy()
}
