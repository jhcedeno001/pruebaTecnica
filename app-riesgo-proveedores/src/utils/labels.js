const FACTOR_LABELS = {
  sin_salida_al_mar: 'Sin salida al mar',
  pocas_fronteras_terrestres: 'Pocas fronteras terrestres',
  conflicto_armado_propio: 'Conflicto armado propio',
  vecino_en_conflicto: 'Vecino en conflicto',
}

const INDICADOR_LABELS = {
  variacion_cambiaria: 'Variación cambiaria',
}

function trasformar(code) {
  if (!code) return ''
  return code
    .replace(/_/g, ' ')
    .replace(/^\w/, (letra) => letra.toUpperCase())
}

export function labelFactor(code) {
  return FACTOR_LABELS[code] ?? trasformar(code)
}

export function labelIndicador(code) {
  return INDICADOR_LABELS[code] ?? trasformar(code)
}
