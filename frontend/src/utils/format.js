/**
 * Shared formatting utilities.
 * Centralizes all presentation logic in one place so components stay clean.
 */

/**
 * Safely formats a price value (float, Decimal string, or number)
 * to a 2-decimal currency string.
 * @param {number|string} value
 * @returns {string} e.g. "19.99"
 */
export function formatPrice(value) {
  return Number(value).toFixed(2)
}

/**
 * Formats an ISO date string to a human-readable date.
 * @param {string} dateString
 * @returns {string} e.g. "July 12, 2024"
 */
export function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

/**
 * Inline SVG data URI used as a fallback when product images fail to load.
 * Avoids depending on external placeholder services (via.placeholder.com, etc.)
 * which can be slow or blocked in some environments.
 */
export const PLACEHOLDER_IMAGE =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Crect fill='%23f3f4f6' width='400' height='400'/%3E%3Ctext fill='%236b7280' font-size='18' font-family='system-ui%2Csans-serif' text-anchor='middle' x='200' y='208'%3ENo Image%3C/text%3E%3C/svg%3E"
