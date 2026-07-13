export default function FactorBar({ aplica }) {
  return (
    <div className="factor-bar" aria-hidden="true">
      <div className={`factor-bar-fill ${aplica ? 'is-active' : ''}`} />
    </div>
  )
}
