import { nivelSlug } from '../utils/nivel'

export default function ScoreBar({ value, max, nivel }) {
  const ratio = max > 0 ? Math.min(Math.max(value / max, 0), 1) : 0
  return (
    <div className="score-bar">
      <div className="score-bar-track">
        <div
          className={`score-bar-fill nivel-fill-${nivelSlug(nivel)}`}
          style={{ width: `${ratio * 100}%` }}
        />
      </div>
      <span className="score-bar-value">{value}</span>
    </div>
  )
}
