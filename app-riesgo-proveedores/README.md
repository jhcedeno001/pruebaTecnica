# app-riesgo-proveedores

Frontend del Panel de Riesgo de Proveedores Internacionales: buscador de riesgo por
país, historial y comparación entre países. Construido con React + Vite.

Usa `npm` como gestor de dependencias.

## Requisitos

- [Node.js](https://nodejs.org/) 22+
- `npm`
- El backend (`api-riesgo-proveedores`) corriendo

## Cómo levantar el proyecto

**1. Instalar dependencias**

```bash
npm install
```

**2. Configurar variables de entorno**

Copiar `.env.example` a `.env`:

```bash
cp .env.example .env
```

| Variable | Descripción |
|---|---|
| `VITE_API_BASE_URL` | URL base del backend (`api-riesgo-proveedores`). |

**3. Levantar el frontend**

```bash
npm run dev
```

Queda escuchando en `http://localhost:5173`.

## Docker

```bash
docker build -t app-riesgo-proveedores:jhcedeno --build-arg VITE_API_BASE_URL=http://localhost:9541 .
```

El contenedor corre en el puerto `80` (nginx).
