const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function request(path) {
  let response
  try {
    response = await fetch(`${BASE_URL}${path}`)
  } catch {
    throw new ApiError(
      'No se pudo conectar con el servidor.',
      0,
    )
  }

  if (!response.ok) {
    let detail = `Error ${response.status}`
    try {
      const body = await response.json()
      if (typeof body?.detail === 'string') detail = body.detail
    } catch {
      console.log("Error para el servidor")
    }
    throw new ApiError(detail, response.status)
  }

  return response.json()
}


export function getCountries() {
  return request('/supplier-risk/countries')
}


export function getHistory(limite = 100) {
  return request(`/supplier-risk/history?limite=${limite}`)
}


export function getRisk(code, { refresh = false } = {}) {
  const query = refresh ? '?refresh=true' : ''
  return request(`/supplier-risk/${encodeURIComponent(code.trim())}${query}`)
}


export function compareCountries(codes) {
  const query = encodeURIComponent(codes.join(','))
  return request(`/supplier-risk/compare?countries=${query}`)
}
