# Generador de Recetas con Inventario

Aplicacion web para registrar ingredientes disponibles en casa y generar recetas estructuradas con un LLM.

## Stack

- Backend: Python, FastAPI, SQLAlchemy, JWT.
- Base de datos: PostgreSQL en desarrollo/despliegue, SQLite solo para pruebas.
- LLM: OpenRouter mediante endpoint OpenAI-compatible.
- Frontend: Vue + Vite en `frontend/`.
- Despliegue: Docker + Docker Compose.

## Configuracion

Ya existe un `.env` local ignorado por Git. Si necesitas regenerarlo:

```bash
copy .env.example .env
```

Para la base local creada como `generador-recetas-llm-db`, ajusta la clave real de PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg2://postgres:TU_PASSWORD@localhost:5432/generador-recetas-llm-db
SECRET_KEY=una-clave-larga-y-secreta
OPENROUTER_API_KEY=sk-or-tu-api-key
OPENROUTER_MODEL=openrouter/free
```

No subas `.env` al repositorio.

## Crear tablas

Con la clave correcta en `.env`, puedes crear/verificar las tablas con:

```bash
python scripts/init_db.py
```

Tambien puedes ejecutar el SQL manual desde pgAdmin:

```txt
database/schema_postgresql.sql
```

Mas detalle: `docs/BACKEND_DATABASE_SETUP.md`.

## Ejecutar backend local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`

Swagger: `http://127.0.0.1:8000/docs`

## Ejecutar frontend local

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://127.0.0.1:5173`

Si el backend no esta en `http://127.0.0.1:8000`, crea `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Ejecutar con Docker Compose

```bash
copy .env.example .env
docker compose up --build
```

Esto levanta:

- API en `http://127.0.0.1:8000`
- PostgreSQL en `127.0.0.1:5432`

## Pruebas

```bash
pytest
```

Las pruebas usan SQLite temporal para no depender de PostgreSQL.

## Entregables

- URL del repositorio.
- URL de produccion con HTTPS.
- PDF de maximo 3 paginas con arquitectura, diagrama ER, decisiones tecnicas y capturas.
