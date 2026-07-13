export default function LoadingState({ message = 'Cargando…' }) {
  return (
    <div className="state state-loading" role="status">
      <span className="spinner" aria-hidden="true" />
      <p>{message}</p>
    </div>
  )
}
