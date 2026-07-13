export function nivelSlug(nivel) {
  return (nivel || '').toLowerCase().trim().replace(/\s+/g, '-')
}
