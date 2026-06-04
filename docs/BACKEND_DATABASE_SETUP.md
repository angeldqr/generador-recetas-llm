# Backend y base de datos

## Estado actual

El backend ya tiene modelos, endpoints, autenticacion JWT, inventario, recetas, calificaciones, cliente LLM por OpenRouter, Docker Compose, tests y archivos de entorno seguros.

Tablas del backend:

- `usuarios`
- `ingredientes`
- `recetas`
- `calificaciones`

## Archivo `.env`

Ya existe un `.env` local en la raiz del proyecto. Ese archivo esta ignorado por Git y no se debe subir.

Antes de correr el backend, cambia esta parte por la clave real de PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg2://recetas_user:recetas_password_dev@localhost:5432/generador-recetas-llm-db
POSTGRES_PASSWORD=recetas_password_dev
```

El usuario local de desarrollo sugerido es `recetas_user`.

## Crear las tablas desde Python

Con la clave correcta en `.env`, ejecuta:

```powershell
.\.venv\Scripts\activate
python scripts\init_db.py
```

Salida esperada:

```txt
Tablas creadas/verificadas: calificaciones, ingredientes, recetas, usuarios
```

## Crear las tablas desde pgAdmin

Si prefieres hacerlo visualmente:

1. Abre pgAdmin.
2. Entra a la base `generador-recetas-llm-db`.
3. Abre Query Tool.
4. Copia el contenido de `database/schema_postgresql.sql`.
5. Ejecuta el script.
6. Verifica que aparezcan las tablas `usuarios`, `ingredientes`, `recetas` y `calificaciones`.

## Correr backend

```powershell
.\.venv\Scripts\activate
uvicorn app.main:app --reload
```

API local:

```txt
http://127.0.0.1:8000/docs
```

## LLM con OpenRouter

El backend ya esta conectado a OpenRouter. Para usar un LLM real:

1. Entra a OpenRouter.
2. Crea una API key.
3. Pegala en `.env`:

```env
OPENROUTER_API_KEY=sk-or-tu-llave-real
OPENROUTER_MODEL=openrouter/free
```

Si `OPENROUTER_API_KEY` esta vacia, el backend usa una receta de prueba para que la demo local no se rompa.
