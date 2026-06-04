# Generador de Recetas con Inventario

Aplicación web full-stack que permite a los usuarios registrar ingredientes disponibles en casa y obtener recetas generadas por un modelo de lenguaje (LLM) a partir de ese inventario. Las recetas se almacenan en base de datos y el usuario puede gestionarlas (calificarlas, guardarlas, eliminarlas).

## Stack Tecnológico

- **Backend:** Python 3.12 + FastAPI + SQLAlchemy + PostgreSQL
- **Frontend:** Vue 3 + TypeScript + Vite + GSAP
- **IA:** OpenRouter (GPT-4o-mini) con prompt engineering estricto
- **Despliegue:** Docker + Docker Compose + Nginx + Ubuntu VPS
- **SSL:** Let's Encrypt con Certbot
- **Tests:** pytest (23 tests)

## Estructura del Proyecto

```
proyecto-recetas/
├── app/                    # Backend FastAPI
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── services/
│       └── llm_service.py
├── frontend/               # Frontend Vue 3
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── router/
│   │   ├── services/
│   │   ├── composables/
│   │   └── styles/
│   └── Dockerfile
├── tests/                  # Tests pytest
├── Dockerfile              # Backend
├── docker-compose.yml      # Orquestación
├── nginx.conf              # Reverse proxy
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

## Variables de Entorno

Copiar `.env.example` a `.env` y completar:

```bash
# Base de datos
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/dbname
POSTGRES_DB=dbname
POSTGRES_USER=user
POSTGRES_PASSWORD=pass

# JWT
SECRET_KEY=tu_clave_secreta_muy_larga
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# OpenRouter
OPENROUTER_API_KEY=sk-or-v1-tu_api_key
OPENROUTER_MODEL=openai/gpt-4o-mini

# Frontend (solo desarrollo)
VITE_API_BASE_URL=http://localhost:8000
```

## Ejecución Local

### 1. Backend

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear .env con las variables necesarias

# Ejecutar servidor
uvicorn app.main:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. Tests

```bash
pytest
```

## Despliegue con Docker (Producción)

### 1. Preparar el servidor VPS

- Ubuntu 22.04/24.04
- Docker y Docker Compose instalados
- Dominio apuntando al VPS (A record)

### 2. Clonar y configurar

```bash
git clone <repo-url>
cd proyecto-recetas
# Crear .env con los valores de producción
nano .env
```

### 3. Construir y desplegar

```bash
docker compose up --build -d
```

### 4. Obtener certificado SSL

```bash
docker run -it --rm \
  -v recetas-certbot_data:/etc/letsencrypt \
  -v recetas-certbot_www:/var/www/certbot \
  certbot/certbot certonly \
  --webroot -w /var/www/certbot \
  -d recetasllm.online -d www.recetasllm.online \
  --agree-tos --no-eff-email --force-renewal
```

### 5. Actualizar Nginx para HTTPS

Modificar `nginx.conf` para incluir los certificados SSL y redirigir HTTP a HTTPS.

## Arquitectura

```
Usuario -> HTTPS -> Nginx
                    ├── /  -> Frontend (Vue static)
                    └── /api/ -> FastAPI
                                   └── PostgreSQL
```

## Funcionalidades

1. Registro e inicio de sesión de usuarios (JWT)
2. CRUD de ingredientes del inventario personal
3. Generar receta a partir del inventario actual (IA)
4. Ver recetas generadas previamente
5. Calificar una receta (1 a 5 estrellas)
6. Eliminar recetas del historial

## Prompt Engineering Estricto

El LLM recibe un prompt con reglas estrictas:
- Usar EXCLUSIVAMENTE los ingredientes del inventario
- NO agregar ingredientes adicionales (sal, aceite, etc.)
- Respetar las cantidades disponibles
- Si no es posible, devolver un JSON con campo `error`

Post-procesamiento: validación fuzzy-match que rechaza recetas con ingredientes extraños.

## Seguridad

- JWT con expiración de 60 minutos
- Contraseñas hasheadas con bcrypt
- CORS restringido en producción
- Variables sensibles en `.env` (nunca en el repo)
- API keys rotadas periódicamente

## Autor

Proyecto final — Tecnologías Web
