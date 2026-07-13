import { nivelSlug } from '../utils/nivel'

export default function NivelBadge({ nivel }) {
  if (!nivel) return null
  return (
    <span className={`badge nivel-${nivelSlug(nivel)}`}>
      <span className="badge-dot" aria-hidden="true" />
      {nivel}
    </span>
  )
}
