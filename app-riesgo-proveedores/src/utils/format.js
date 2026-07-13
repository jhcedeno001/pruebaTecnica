export function formatNumber(value, opts) {
  if (value === null || value === undefined) return '—'
  return new Intl.NumberFormat('es', opts).format(value)
}

export function formatFecha(iso) {
  try {
    return new Intl.DateTimeFormat('es', { dateStyle: 'medium', timeStyle: 'short' }).format(
      new Date(iso),
    )
  } catch {
    return iso
  }
}
