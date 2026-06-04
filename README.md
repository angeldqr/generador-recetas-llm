# Generador de Recetas con Inventario

Aplicación web para registrar ingredientes disponibles en casa y generar recetas estructuradas con un LLM.

## Stack

- Backend: Python, FastAPI, SQLAlchemy, JWT.
- Base de datos: MySQL en desarrollo/despliegue, SQLite solo para pruebas.
- LLM: OpenRouter mediante endpoint OpenAI-compatible.
- Frontend: Vue + Vite en `frontend/`.
- Despliegue: Docker + Docker Compose.

## Configuración

1. Copia las variables de ejemplo.

```bash
copy .env.example .env
```

2. Ajusta `.env`.

Para tu base local creada como `generador-recetas-llm-db`, usa algo como:

```env
DATABASE_URL=mysql+pymysql://root:TU_PASSWORD@localhost:3306/generador-recetas-llm-db
SECRET_KEY=una-clave-larga-y-secreta
OPENROUTER_API_KEY=sk-or-tu-api-key
OPENROUTER_MODEL=openrouter/free
```

No subas `.env` al repositorio.

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

Si el backend no está en `http://127.0.0.1:8000`, crea `frontend/.env`:

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
- MySQL en `127.0.0.1:3306`

## Pruebas

```bash
pytest
```

Las pruebas usan SQLite temporal para no depender de MySQL.

## Entregables

- URL del repositorio.
- URL de producción con HTTPS.
- PDF de máximo 3 páginas con arquitectura, diagrama ER, decisiones técnicas y capturas.
