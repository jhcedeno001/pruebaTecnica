import CountryFlag from '../../components/CountryFlag'
import NivelBadge from '../../components/NivelBadge'
import ScoreMeter from '../../components/ScoreMeter'
import FactorBar from '../../components/FactorBar'
import { labelFactor, labelIndicador } from '../../utils/labels'
import { formatNumber } from '../../utils/format'
import { PUNTOS_BUCKET_ECONOMICO_MAXIMO } from '../../utils/constants'

export default function RiskResult({ result, onRefresh, refreshing }) {
  const {
    pais,
    riesgo_geopolitico: geo,
    riesgo_economico: eco,
    score_total,
    nivel_combinado,
  } = result
  const scoreMaximoCombinado = geo.score_maximo + PUNTOS_BUCKET_ECONOMICO_MAXIMO

  return (
    <div className="risk-result">
      <header className="risk-header">
        <div className="risk-header-country">
          <CountryFlag alpha2={pais.alpha2} alt={pais.nombre} />
          <div>
            <h2>{pais.nombre}</h2>
            <p className="muted">
              {pais.alpha2} / {pais.alpha3} · {pais.region || 'Región desconocida'}
              {pais.subregion ? ` · ${pais.subregion}` : ''}
            </p>
          </div>
        </div>
        <div className="risk-header-score">
          <div className="score-total-meter">
            <ScoreMeter value={score_total} max={scoreMaximoCombinado} nivel={nivel_combinado} />
            <div className="score-total-label">
              <span className="score-total-caption">Riesgo combinado</span>
              <NivelBadge nivel={nivel_combinado} />
            </div>
          </div>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onRefresh}
            disabled={refreshing}
          >
            {refreshing ? 'Actualizando…' : 'Actualizar datos'}
          </button>
        </div>
      </header>

      <dl className="country-facts">
        <div>
          <dt>Población</dt>
          <dd>{formatNumber(pais.poblacion)}</dd>
        </div>
        <div>
          <dt>Área</dt>
          <dd>{pais.area ? `${formatNumber(pais.area)} km²` : '—'}</dd>
        </div>
        <div>
          <dt>Densidad</dt>
          <dd>
            {pais.poblacion_densidad
              ? `${formatNumber(pais.poblacion_densidad, { maximumFractionDigits: 1 })} personas por km²`
              : '—'}
          </dd>
        </div>
        <div>
          <dt>Moneda</dt>
          <dd>{pais.moneda || '—'}</dd>
        </div>
        <div>
          <dt>Fronteras terrestres</dt>
          <dd>{pais.fronteras.length}</dd>
        </div>
      </dl>

      <section className="risk-card">
        <div className="risk-card-header">
          <h3>Riesgo geopolítico</h3>
          <NivelBadge nivel={geo.nivel} />
          <ScoreMeter value={geo.score_total} max={geo.score_maximo} nivel={geo.nivel} size={44} strokeWidth={5} />
        </div>
        <table className="risk-table">
          <thead>
            <tr>
              <th>Factor</th>
              <th>Descripción</th>
              <th>Aplica</th>
              <th>Puntos</th>
            </tr>
          </thead>
          <tbody>
            {geo.desglose.map((factor) => (
              <tr key={factor.factor} className={factor.aplica ? 'factor-aplica' : ''}>
                <td>{labelFactor(factor.factor)}</td>
                <td>{factor.descripcion}</td>
                <td>
                  <FactorBar aplica={factor.aplica} />
                  <span className="sr-only">{factor.aplica ? 'Aplica' : 'No aplica'}</span>
                </td>
                <td>{factor.puntos}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="risk-card">
        <div className="risk-card-header">
          <h3>Riesgo económico</h3>
          <NivelBadge nivel={eco.nivel} />
          <ScoreMeter
            value={Math.round(eco.score)}
            max={100}
            nivel={eco.nivel}
            size={44}
            strokeWidth={5}
          />
        </div>
        <p className="recomendacion">{eco.recomendacion}</p>
        <table className="risk-table">
          <thead>
            <tr>
              <th>Indicador</th>
              <th>Valor</th>
              <th>Disponible</th>
              <th>Puntos</th>
              <th>Peso</th>
            </tr>
          </thead>
          <tbody>
            {eco.indicadores.map((ind) => (
              <tr key={ind.nombre}>
                <td>{labelIndicador(ind.nombre)}</td>
                <td>
                  {ind.disponible
                    ? `${formatNumber(ind.valor, { maximumFractionDigits: 2 })} ${ind.unidad}`
                    : '—'}
                </td>
                <td>{ind.disponible ? 'Sí' : 'No'}</td>
                <td>{formatNumber(ind.puntos, { maximumFractionDigits: 1 })}</td>
                <td>{formatNumber(ind.peso * 100, { maximumFractionDigits: 0 })}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  )
}
