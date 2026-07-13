import { useState } from 'react'
import BuscarView from './views/BuscarView'
import HistorialView from './views/HistorialView'
import CompararView from './views/CompararView'
import './App.css'

const VIEWS = [
  { id: 'buscar', label: 'Buscar', Component: BuscarView },
  { id: 'historial', label: 'Historial', Component: HistorialView },
  { id: 'comparar', label: 'Comparar', Component: CompararView },
]

function App() {
  const [activeView, setActiveView] = useState('buscar')
  const ActiveComponent = VIEWS.find((view) => view.id === activeView)?.Component ?? BuscarView

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-inner">
          <div className="app-brand">
            <h1 className="app-title">Panel de Riesgo de Proveedores Internacionales</h1>
          </div>
          <nav className="app-nav">
            {VIEWS.map((view) => (
              <button
                key={view.id}
                type="button"
                className={`nav-tab ${activeView === view.id ? 'active' : ''}`}
                onClick={() => setActiveView(view.id)}
              >
                {view.label}
              </button>
            ))}
          </nav>
        </div>
      </header>
      <main className="app-main">
        <ActiveComponent />
      </main>
    </div>
  )
}

export default App
