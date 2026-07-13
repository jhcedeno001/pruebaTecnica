import { useState } from 'react'
import { useCountries } from '../hooks/useCountries'

export default function CountrySearch({ onSearch, loading }) {
  const [value, setValue] = useState('')
  const { countries, resolveCode } = useCountries()

  function handleSubmit(event) {
    event.preventDefault()
    const trimmed = value.trim()
    if (!trimmed) return
    onSearch(resolveCode(trimmed))
  }

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="search-form-row">
        <div className="search-field">
          <label htmlFor="country-code">País</label>
          <input
            id="country-code"
            list="known-countries"
            type="text"
            placeholder="Ecuador, EC…"
            value={value}
            onChange={(event) => setValue(event.target.value)}
            autoComplete="off"
          />
          <datalist id="known-countries">
            {countries.map((pais) => (
              <option key={pais.codigo_alfa2} value={pais.nombre} />
            ))}
          </datalist>
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading || !value.trim()}>
          {loading ? 'Buscando…' : 'Buscar'}
        </button>
      </div>
      <p className="search-hint">Buscá por nombre del país (ej: Ecuador) o por su código (ej: EC).</p>
    </form>
  )
}
