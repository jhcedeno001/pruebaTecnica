# api-riesgo-proveedores

API del Panel de Riesgo de Proveedores Internacionales: evalúa el riesgo geopolítico y
económico de un país proveedor. Construida con FastAPI + SQLAlchemy async.

Usa [uv](https://docs.astral.sh/uv/) como gestor de dependencias.

El contrato de la API está en [`api-riesgo-proveedores.yaml`](./api-riesgo-proveedores.yaml) (OpenAPI).

## Requisitos

- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado
- Python 3.14+
- Usa Postgres

## Cómo levantar el proyecto

**1. Instalar dependencias**

```bash
uv sync
```

**2. Configurar variables de entorno**

Copiar `.env.dist` a `.env`:

```bash
cp .env.dist .env
```

Completar en `.env` los datos de conexión a Postgres (`DB_HOST`, `DB_PORT`, `DB_NAME`,
`DB_USER`, `DB_PASSWORD`). El resto de las variables ya trae valores por defecto:

| Variable | Descripción |
|---|---|
| `APP_NAME` | Nombre de la app, aparece en `/docs`. |
| `DEBUG` | Modo debug de FastAPI. |
| `CORS_ORIGINS` | Orígenes permitidos para CORS (lista JSON). |
| `DB_HOST` | Host de Postgres. |
| `DB_PORT` | Puerto de Postgres. |
| `DB_NAME` | Nombre de la base de datos. |
| `DB_USER` | Usuario de Postgres. |
| `DB_PASSWORD` | Contraseña de Postgres. |
| `COUNTRIES_API_BASE_URL` | URL base de countries.dev (datos de países). |
| `COUNTRIES_API_TIMEOUT_SECONDS` | Timeout para las llamadas a countries.dev. |
| `EXCHANGE_RATE_PRIMARY_URL` | URL principal de la API de tipos de cambio. |
| `EXCHANGE_RATE_FALLBACK_URL` | URL alternativa si la principal falla. |
| `EXCHANGE_RATE_API_TIMEOUT_SECONDS` | Timeout para las llamadas de tipo de cambio. |
| `GEO_REFERENCE_DATASET_URL` | Dataset (mledoze/countries) usado para el factor "sin salida al mar". |
| `GEO_REFERENCE_API_TIMEOUT_SECONDS` | Timeout para ese dataset. |
| `CONFLICTS_DATASET_URL` | Dataset de conflictos armados activos por país (Our World in Data). |
| `CONFLICTS_API_TIMEOUT_SECONDS` | Timeout para ese dataset. |
| `HTTP_BREAKER_FAIL_MAX` | Fallas seguidas antes de abrir el circuit breaker de los clientes HTTP. |
| `HTTP_BREAKER_RESET_TIMEOUT_SECONDS` | Segundos antes de reintentar tras abrirse el breaker. |
| `HTTP_RATE_LIMIT_PER_SECOND` | Límite de requests por segundo hacia cada API externa. |

**3. Levantar la API**

```bash
uv run uvicorn app.main:app
```

Al arrancar crea las tablas que falten en Postgres. Queda escuchando en
`http://localhost:8000` (docs interactivas en `/docs`).

## Docker

```bash
docker build -t api-riesgo-proveedores:jhcedeno .
```

El contenedor corre en el puerto `9541`.
