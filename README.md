# API Biblioteca

## Requisitos
- Python 3.11+
- PostgreSQL o SQLite

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración
Copia `.env.example` y ajusta la base de datos:

```bash
copy .env.example .env
```

### PostgreSQL con Docker

```bash
docker compose up -d
```

La configuración de `.env` se comparte con Docker Compose:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/biblioteca
POSTGRES_DB=biblioteca
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

### SQLite para pruebas rápidas

```env
DATABASE_URL=sqlite:///./biblioteca.db
```

## Ejecutar

```bash
uvicorn app.main:app --reload
```

Documentación:
http://127.0.0.1:8000/docs

## Endpoints

### Autores
- GET /autores
- GET /autores/{id}
- POST /autores
- PATCH /autores/{id}
- DELETE /autores/{id}

### Libros
- GET /libros
- GET /libros/{id}
- POST /libros
- PATCH /libros/{id}
- DELETE /libros/{id}
