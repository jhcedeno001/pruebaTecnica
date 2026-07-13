# pruebaTecnica

Panel de Riesgo de Proveedores Internacionales — backend (`api-riesgo-proveedores`),
frontend (`app-riesgo-proveedores`) y Postgres.

## Arquitectura

El backend (FastAPI + SQLAlchemy async, con [uv](https://docs.astral.sh/uv/) como gestor
de dependencias) sigue una arquitectura por capas: endpoints → services → repositories →
clients, y expone una API REST consumida por el frontend (React + Vite). Los datos persisten en Postgres. 

## Cómo correr el proyecto con Docker

**Requisitos:** Docker y Docker Compose.

**1. Construir las imágenes**

```bash
docker build -t api-riesgo-proveedores:jhcedeno ./api-riesgo-proveedores
docker build -t app-riesgo-proveedores:jhcedeno --build-arg VITE_API_BASE_URL=http://localhost:9541 ./app-riesgo-proveedores
```

**2. Levantar todo (Postgres + backend + frontend)**

```bash
docker compose up -d
```

## Servicios

| Servicio | URL |
|---|---|
| Frontend | http://localhost:9642 |
| Backend | http://localhost:9541 (docs en `/docs`) |
| Postgres | localhost:5433 |

## Cómo correr el proyecto sin Docker

**Requisitos:** [uv](https://docs.astral.sh/uv/), Node.js 22+ con `npm`, y un Postgres local.

**1. Backend**

```bash
cd api-riesgo-proveedores
uv sync
cp .env.dist .env
uv run uvicorn app.main:app
```

**2. Frontend** (en otra terminal)

```bash
cd app-riesgo-proveedores
npm install
cp .env.example .env
npm run dev
```

## Variables de entorno

Cada servicio trae su propia plantilla: `.env.dist` en `api-riesgo-proveedores` (datos de
Postgres, timeouts y URLs de las 4 APIs externas) y `.env.dist` en `app-riesgo-proveedores`
(`VITE_API_BASE_URL`). El detalle de cada variable está en el README de cada subproyecto.

## Contrato de la API

Definido en [`api-riesgo-proveedores/api-riesgo-proveedores.yaml`](./api-riesgo-proveedores/api-riesgo-proveedores.yaml) (OpenAPI).
