import type { CSSProperties } from 'vue'

interface AnchoredTargetOptions {
  width?: number
  height?: number
  margin?: number
  gap?: number
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

  const margin = options.margin ?? 16
  const gap = options.gap ?? 12
  const viewport = window.visualViewport
  const viewportWidth = viewport?.width ?? window.innerWidth
  const viewportHeight = viewport?.height ?? window.innerHeight
  const targetWidth = Math.min(
    options.width ?? 540,
    viewportWidth - margin * 2,
  )
  const targetHeight = Math.min(
    options.height ?? 560,
    viewportHeight - margin * 2,
  )

  if (!trigger) {
    return {
      left: `${(viewportWidth - targetWidth) / 2}px`,
      top: `${(viewportHeight - targetHeight) / 2}px`,
      width: `${targetWidth}px`,
      maxHeight: `calc(100dvh - ${margin * 2}px)`,
      '--blendy-origin-x': '50%',
      '--blendy-origin-y': '50%',
    } as CSSProperties
  }

  const rect = trigger.getBoundingClientRect()
  const triggerCenterX = rect.left + rect.width / 2
  const triggerCenterY = rect.top + rect.height / 2

  document.documentElement.style.setProperty(
    '--blendy-backdrop-x',
    `${triggerCenterX}px`,
  )
  document.documentElement.style.setProperty(
    '--blendy-backdrop-y',
    `${triggerCenterY}px`,
  )

  let left = triggerCenterX - targetWidth / 2

  if (triggerCenterX < viewportWidth * 0.36) {
    left = rect.left
  }

  if (triggerCenterX > viewportWidth * 0.64) {
    left = rect.right - targetWidth
  }

  left = clamp(left, margin, viewportWidth - targetWidth - margin)

  const roomBelow = viewportHeight - rect.bottom - margin
  const roomAbove = rect.top - margin
  let top = rect.bottom + gap

  if (roomBelow < targetHeight + gap && roomAbove > roomBelow) {
    top = rect.top - targetHeight - gap
  }

  if (top < margin || top + targetHeight > viewportHeight - margin) {
    top = triggerCenterY - targetHeight / 2
  }

  top = clamp(top, margin, viewportHeight - targetHeight - margin)

  return {
    left: `${left}px`,
    top: `${top}px`,
    width: `${targetWidth}px`,
    maxHeight: `calc(100dvh - ${margin * 2}px)`,
    '--blendy-origin-x': `${triggerCenterX - left}px`,
    '--blendy-origin-y': `${triggerCenterY - top}px`,
    '--blendy-source-width': `${rect.width}px`,
    '--blendy-source-height': `${rect.height}px`,
  } as CSSProperties
}
