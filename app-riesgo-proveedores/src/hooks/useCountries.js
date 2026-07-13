import { useEffect, useState } from 'react'
import { getCountries } from '../api/client'

export function useCountries() {
  const [countries, setCountries] = useState([])

  useEffect(() => {
    getCountries()
      .then(setCountries)
      .catch(() => setCountries([]))
  }, [])

  function resolveCode(text) {
    const match = countries.find(
      (pais) => pais.nombre.toLowerCase() === text.toLowerCase()
    )
    return match ? match.codigo_alfa2 : text.toUpperCase()
  }

  return { countries, resolveCode }
}
