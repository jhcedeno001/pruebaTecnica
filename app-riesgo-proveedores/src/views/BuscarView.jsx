import { useState } from 'react'
import CountrySearch from '../components/CountrySearch'
import RiskResult from '../features/riesgo/RiskResult'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'
import { getRisk } from '../api/client'

export default function BuscarView() {
  const [status, setStatus] = useState('idle') // idle | loading | refreshing | success | error
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [lastCode, setLastCode] = useState('')

  async function search(code, { refresh = false } = {}) {
    setStatus(refresh ? 'refreshing' : 'loading')
    setError(null)
    setLastCode(code)
    try {
      const data = await getRisk(code, { refresh })
      setResult(data)
      setStatus('success')
    } catch (err) {
      setResult(null)
      setError(err)
      setStatus('error')
    }
  }

  return (
    <section className="view">
      <h1>Buscar riesgo de un proveedor por país</h1>
      <p className="muted">Escribí el nombre o el código del país del proveedor.</p>
      <CountrySearch onSearch={search} loading={status === 'loading'} />

      {status === 'loading' && <LoadingState message={`Consultando ${lastCode}…`} />}
      {status === 'error' && (
        <ErrorState message={error.message} onRetry={() => search(lastCode)} />
      )}
      {(status === 'success' || status === 'refreshing') && result && (
        <RiskResult
          result={result}
          refreshing={status === 'refreshing'}
          onRefresh={() => search(lastCode, { refresh: true })}
        />
      )}
    </section>
  )
}
