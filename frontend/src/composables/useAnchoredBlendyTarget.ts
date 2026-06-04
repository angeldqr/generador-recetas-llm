import type { CSSProperties } from 'vue'

interface AnchoredTargetOptions {
  width?: number
  height?: number
  margin?: number
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max)
}

export function buildAnchoredBlendyTargetStyle(
  blendyId: string,
  options: AnchoredTargetOptions = {},
): CSSProperties {
  if (typeof window === 'undefined') return {}

  const trigger = document.querySelector<HTMLElement>(
    `[data-blendy-from="${blendyId}"]`,
  )

  if (!trigger) return {}

  const margin = options.margin ?? 16
  const rect = trigger.getBoundingClientRect()
  const viewportWidth = window.innerWidth
  const viewportHeight = window.innerHeight
  const targetWidth = Math.min(
    options.width ?? 540,
    viewportWidth - margin * 2,
  )
  const targetHeight = Math.min(
    options.height ?? 560,
    viewportHeight - margin * 2,
  )

  let left = rect.left + rect.width / 2 - targetWidth / 2

  if (rect.left < viewportWidth * 0.34) {
    left = rect.left
  }

  if (rect.right > viewportWidth * 0.66) {
    left = rect.right - targetWidth
  }

  left = clamp(left, margin, viewportWidth - targetWidth - margin)

  let top = rect.bottom + 12

  if (top + targetHeight > viewportHeight - margin) {
    top = rect.top - targetHeight - 12
  }

  if (top < margin) {
    top = rect.top + rect.height / 2 - targetHeight / 2
  }

  top = clamp(top, margin, viewportHeight - targetHeight - margin)

  return {
    left: `${left}px`,
    top: `${top}px`,
    width: `${targetWidth}px`,
    maxHeight: `calc(100dvh - ${margin * 2}px)`,
    '--blendy-origin-x': `${rect.left + rect.width / 2 - left}px`,
    '--blendy-origin-y': `${rect.top + rect.height / 2 - top}px`,
  } as CSSProperties
}
