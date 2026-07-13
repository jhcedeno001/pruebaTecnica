import { nivelSlug } from '../utils/nivel'

export default function ScoreMeter({ value, max, nivel, size = 84, strokeWidth = 8 }) {
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const ratio = max > 0 ? Math.min(Math.max(value / max, 0), 1) : 0
  const offset = circumference * (1 - ratio)

  return (
    <div className="score-meter" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle
          className="score-meter-track"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          fill="none"
        />
        <circle
          className={`score-meter-value nivel-stroke-${nivelSlug(nivel)}`}
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
      </svg>
      <div className="score-meter-label">
        <span className="score-meter-value-text">{value}</span>
        <span className="score-meter-max-text">/{max}</span>
      </div>
    </div>
  )
}
