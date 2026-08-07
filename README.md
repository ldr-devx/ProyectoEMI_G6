# Plataforma de Empleo USAC — ProyectoEMI G6

Bolsa de trabajo segmentada para la comunidad académica de la **Facultad de Ingeniería, USAC**. Conecta estudiantes y egresados con empresas y referidores de la misma comunidad académica.

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11 · FastAPI · SQLAlchemy |
| Base de datos | SQLite (dev) |
| Auth | JWT via python-jose · bcrypt |
| Frontend | HTML5 · CSS (Industry DS) · JavaScript ES6+ vanilla |

## Levantar el proyecto (primera vez)

### 1. Prerrequisitos
- Python 3.11+
- Git

### 2. Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Variables de entorno (el default funciona para dev)
cp env.example .env

# Poblar BD con datos de prueba
python seed.py

# Iniciar servidor
python run.py
```

El servidor corre en **http://localhost:8000**

- Frontend: http://localhost:8000
- API Swagger: http://localhost:8000/api/docs

## Usuarios de prueba (tras seed.py)

| Email | Contraseña | Rol |
|-------|-----------|-----|
| estudiante@usac.edu.gt | password123 | Estudiante |
| empresa@techgt.com | password123 | Empresa |
| referidor@gmail.com | password123 | Referidor |
| moderador@usac.edu.gt | password123 | Moderador |

## Estructura

```
ProyectoEMI_G6/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI app + rutas
│   │   ├── config.py      # Settings (env vars)
│   │   ├── database.py    # SQLAlchemy + SQLite
│   │   ├── models/        # Modelos (tablas)
│   │   ├── schemas/       # Pydantic (request/response)
│   │   ├── routers/       # Endpoints por dominio
│   │   └── core/          # JWT, seguridad, deps
│   ├── seed.py            # Datos de prueba
│   ├── run.py             # Entrypoint uvicorn
│   └── requirements.txt
├── frontend/
│   ├── index.html         # Landing
│   ├── login.html         # Login
│   ├── pages/             # Páginas por rol
│   ├── js/api.js          # Cliente HTTP
│   ├── js/auth.js         # JWT + guards
│   └── _ds/               # Industry Design System
├── design/                # Prototipo original (referencia)
└── docs/SPRINTS.md        # Plan de 5 sprints
```

## Flujo de ramas

```
main              ← siempre estable
sprint-N/feature  ← una rama por feature
```

Ver [`docs/SPRINTS.md`](docs/SPRINTS.md) para el plan completo.
