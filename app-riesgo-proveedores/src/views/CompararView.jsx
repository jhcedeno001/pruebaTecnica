import { useState } from 'react'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'
import CountryFlag from '../components/CountryFlag'
import NivelBadge from '../components/NivelBadge'
import ScoreMeter from '../components/ScoreMeter'
import { ApiError, compareCountries } from '../api/client'
import { useCountries } from '../hooks/useCountries'
import { SCORE_TOTAL_MAXIMO } from '../utils/constants'

const MIN_PAISES = 2
const MAX_PAISES = 3

export default function CompararView() {
  const [codes, setCodes] = useState(Array(MAX_PAISES).fill(''))
  const [status, setStatus] = useState('idle')
  const [items, setItems] = useState([])
  const [error, setError] = useState(null)
  const { countries, resolveCode } = useCountries()

  function updateCode(index, value) {
    setCodes((prev) => prev.map((code, i) => (i === index ? value : code)))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const cleaned = codes.map((code) => code.trim()).filter(Boolean).map(resolveCode)
    if (cleaned.length < MIN_PAISES) {
      setError(new ApiError(`Ingresá al menos ${MIN_PAISES} países para comparar.`, 0))
      setStatus('error')
      return
    }

    setStatus('loading')
    setError(null)
    try {
      const data = await compareCountries(cleaned)
      setItems(data)
      setStatus('success')
    } catch (err) {
      setError(err)
      setStatus('error')
    }
  }

  return (
    <section className="view">
      <h1>Comparar proveedores por país</h1>
      <p className="muted">
        Ingresá entre {MIN_PAISES} y {MAX_PAISES} países, por nombre o código.
      </p>

      <form className="compare-form" onSubmit={handleSubmit}>
        {codes.map((code, index) => (
          <input
            key={index}
            type="text"
            list="known-countries-compare"
            autoComplete="off"
            placeholder={`País ${index + 1} (ej: Ecuador o EC)`}
            value={code}
            onChange={(event) => updateCode(index, event.target.value)}
          />
        ))}
        <datalist id="known-countries-compare">
          {countries.map((pais) => (
            <option key={pais.codigo_alfa2} value={pais.nombre} />
          ))}
        </datalist>
        <button type="submit" className="btn btn-primary" disabled={status === 'loading'}>
          {status === 'loading' ? 'Comparando…' : 'Comparar'}
        </button>
      </form>

      {status === 'loading' && <LoadingState message="Comparando países…" />}
      {status === 'error' && <ErrorState message={error.message} />}
      {status === 'success' && (
        <div className="compare-grid">
          {items.map((item) => (
            <div
              key={item.codigo_solicitado}
              className={`compare-card ${item.ok ? '' : 'compare-card-error'}`}
            >
              {item.ok ? (
                <>
                  <div className="compare-card-header">
                    <CountryFlag alpha2={item.pais_alpha2} alt={item.pais_nombre} />
                    <h3>{item.pais_nombre}</h3>
                  </div>
                  <div className="compare-score">
                    <ScoreMeter
                      value={item.score_total}
                      max={SCORE_TOTAL_MAXIMO}
                      nivel={item.nivel_combinado}
                      size={56}
                      strokeWidth={6}
                    />
                    <NivelBadge nivel={item.nivel_combinado} />
                  </div>
                  <dl className="compare-facts">
                    <div>
                      <dt>Geopolítico</dt>
                      <dd>{item.score_geopolitico}</dd>
                    </div>
                    <div>
                      <dt>Económico</dt>
                      <dd>{Number(item.score_economico).toFixed(1)}</dd>
                    </div>
                  </dl>
                </>
              ) : (
                <>
                  <h3>{item.codigo_solicitado}</h3>
                  <p className="error-text">{item.error}</p>
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </section>
  )
}
