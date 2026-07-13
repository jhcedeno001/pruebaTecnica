import { useCallback, useEffect, useState } from 'react'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'
import CountryFlag from '../components/CountryFlag'
import NivelBadge from '../components/NivelBadge'
import ScoreBar from '../components/ScoreBar'
import { getHistory } from '../api/client'
import { formatFecha } from '../utils/format'
import { SCORE_TOTAL_MAXIMO } from '../utils/constants'

export default function HistorialView() {
  const [status, setStatus] = useState('loading')
  const [items, setItems] = useState([])
  const [error, setError] = useState(null)

  const load = useCallback(async () => {
    setStatus('loading')
    setError(null)
    try {
      const data = await getHistory(100)
      setItems(data)
      setStatus('success')
    } catch (err) {
      setError(err)
      setStatus('error')
    }
  }, [])

  useEffect(() => {
    load()
  }, [load])

  return (
    <section className="view">
      <div className="view-header">
        <div>
          <h1>Historial de consultas</h1>
          <p className="muted">Países que ya consultaste antes.</p>
        </div>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={load}
          disabled={status === 'loading'}
        >
          Refrescar
        </button>
      </div>

      {status === 'loading' && <LoadingState message="Cargando historial…" />}
      {status === 'error' && <ErrorState message={error.message} onRetry={load} />}
      {status === 'success' && items.length === 0 && (
        <p className="muted">Todavía no se consultó ningún país.</p>
      )}
      {status === 'success' && items.length > 0 && (
        <table className="history-table">
          <thead>
            <tr>
              <th aria-hidden="true"></th>
              <th>País</th>
              <th>Score</th>
              <th>Nivel</th>
              <th>Consultado</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, index) => (
              <tr key={`${item.pais_alpha2}-${item.consultado_en}-${index}`}>
                <td>
                  {item.pais_bandera_url ? (
                    <img className="flag" src={item.pais_bandera_url} alt="" loading="lazy" />
                  ) : (
                    <CountryFlag alpha2={item.pais_alpha2} />
                  )}
                </td>
                <td>
                  {item.pais_nombre} <span className="muted">({item.pais_alpha2})</span>
                </td>
                <td>
                  <ScoreBar
                    value={item.score_total}
                    max={SCORE_TOTAL_MAXIMO}
                    nivel={item.nivel_combinado}
                  />
                </td>
                <td>
                  <NivelBadge nivel={item.nivel_combinado} />
                </td>
                <td>{formatFecha(item.consultado_en)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}
