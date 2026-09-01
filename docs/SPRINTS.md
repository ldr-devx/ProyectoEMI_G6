# Plan de Desarrollo — Plataforma de Empleo USAC

> **5 sprints autoconclusivos** — cada uno entrega un slice vertical funcional y desplegable. Al terminar cada sprint, la aplicación corre y es demostrable. Los sprints están diseñados para que 3-5 personas trabajen en paralelo sin pisarse.

> **Estado actual: TODOS LOS SPRINTS COMPLETADOS ✅**

---

>[!info] Para levantar el proyecto:
  cd backend
  python -m venv venv && source venv/bin/activate
  pip install -r requirements.txt
  cp env.example .env
  python seed.py
  python run.py
  http://localhost:8000

---

## Arquitectura general

```
┌─────────────────────────────────────────────────┐
│  Frontend (HTML + JS vanilla + Industry DS)      │
│  http://localhost:8000/                          │
│                                                  │
│  js/api.js   ──►  fetch("/api/...")              │
│  js/auth.js  ──►  localStorage JWT + guards      │
│  js/notif.js ──►  badge de notificaciones        │
└──────────────────────┬──────────────────────────┘
                       │ HTTP / REST
┌──────────────────────▼──────────────────────────┐
│  Backend (FastAPI · Python 3.14)                 │
│  http://localhost:8000/api/...                   │
│  Swagger: http://localhost:8000/api/docs         │
│                                                  │
│  routers/auth.py              /api/auth/*        │
│  routers/usuarios.py          /api/usuarios/*    │
│  routers/vacantes.py          /api/vacantes/*    │
│  routers/postulaciones.py     /api/postulaciones/*│
│  routers/moderacion.py        /api/moderacion/*  │
│  routers/notificaciones.py    /api/notificaciones/*│
│  routers/certificaciones.py   /api/certificaciones/*│
└──────────────────────┬──────────────────────────┘
                       │ SQLAlchemy ORM
┌──────────────────────▼──────────────────────────┐
│  SQLite  ·  usac_empleos.db  (local, en .gitignore)│
└─────────────────────────────────────────────────┘
```

## Modelo de datos completo

```
usuarios            vacantes             postulaciones
──────────          ────────             ─────────────
id (PK)             id (PK)              id (PK)
email               tipo                 estudiante_id → usuarios.id
password_hash       publicador_id → id   vacante_id → vacantes.id
tipo_usuario        puesto               estado
nivel_verificacion  empresa_nombre       nota_empresa
nombre              carrera_compatible   created_at
carrera             semestre_minimo
semestre            modalidad            certificaciones
creditos_aprobados  tipo_contrato        ───────────────
estado_academico    ubicacion            id (PK)
bio / cv_url        descripcion          usuario_id → usuarios.id
github_url          requisitos           tipo
nombre_empresa      nota_personal        nombre
sector              enlace_oficial       entidad_emisora
sitio_web           solo_plataforma      fecha_obtencion
carrera_egresada    exclusiva_hasta      url_verificacion
is_active           nivel_minimo_req     estado
created_at          estado
                    created_at           notificaciones
                                         ──────────────
                                         id (PK)
                                         usuario_id → usuarios.id
                                         tipo
                                         titulo / mensaje
                                         leida
                                         referencia_id
                                         created_at
```

## Convenciones del equipo

- **Branches:** `sprint-N/nombre-feature` (ej. `sprint-1/auth-backend`)
- **Commits:** prefijos convencionales — `feat:`, `fix:`, `chore:`, `docs:`
- **PRs:** mínimo 1 revisión antes de merge a `main`
- **`.env` nunca va en git.** Usar `env.example` como referencia.
- **Cada endpoint en su router.** No agregar lógica en `main.py`.
- **Cada modelo en su archivo.** No mezclar modelos.
- **La BD local es de cada quien.** No compartir el `.db`. El `seed.py` recrea los datos.

---

## Sprint 1 — Fundación: Backend + Auth + Estructura ✅ COMPLETO

**Objetivo:** El proyecto corre localmente. Cualquier miembro del equipo puede registrarse y hacer login.

### Resultado
> "Abrimos `http://localhost:8000`, nos registramos como estudiante, el sistema nos devuelve un JWT, y hacemos login con esas credenciales. La página de inicio carga con el design system."

### Entregado

#### Backend ✅
- [x] Estructura de carpetas completa
- [x] `backend/app/models/` — todos los modelos SQLAlchemy
- [x] `backend/app/schemas/auth.py` — schemas de registro/login
- [x] `backend/app/routers/auth.py` — `/api/auth/registro` y `/api/auth/login`
- [x] `backend/app/core/security.py` — bcrypt + JWT
- [x] `backend/app/core/deps.py` — `get_current_user`, `require_role`
- [x] `backend/app/main.py` — app FastAPI con rutas y static files
- [x] `backend/seed.py` — datos de prueba

#### Frontend ✅
- [x] `frontend/index.html` — landing con selector de rol y 4 tarjetas
- [x] `frontend/login.html` — formulario de login funcional
- [x] `frontend/js/api.js` — cliente HTTP con manejo de JWT
- [x] `frontend/js/auth.js` — JWT storage + guards + redirectToDashboard
- [x] `frontend/pages/registro/estudiante.html` — formulario multi-step (3 pasos)
- [x] `frontend/pages/registro/empresa.html` — registro de empresa
- [x] `frontend/pages/registro/referidor.html` — registro de referidor
- [x] `frontend/pages/estudiante/home.html` — dashboard stub
- [x] `frontend/pages/empresa/home.html` — dashboard stub
- [x] `frontend/pages/referidor/home.html` — dashboard stub
- [x] `frontend/pages/moderador/home.html` — dashboard stub

### Endpoints disponibles

| Método | Ruta | Body | Respuesta |
|--------|------|------|-----------|
| POST | `/api/auth/registro` | `{email, password, tipo_usuario, nombre}` | `{access_token, tipo_usuario, user_id, nombre}` |
| POST | `/api/auth/login` | `{email, password}` | `{access_token, tipo_usuario, user_id, nombre}` |

---

## Sprint 2 — Perfiles de Usuario + Dashboards por Rol ✅ COMPLETO

**Objetivo:** Cada usuario puede ver y editar su perfil completo. Los dashboards muestran información real.

### Resultado
> "El estudiante Ana entra a su perfil, completa su carrera, semestre y bio, y la barra de créditos muestra su progreso. La empresa ve su nombre y sector. El referidor ve su carrera egresada."

### Entregado

#### Backend ✅ (ya estaba implementado)
- [x] `GET /api/usuarios/me` — perfil completo autenticado
- [x] `PUT /api/usuarios/me` — actualización parcial de perfil
- [x] `GET /api/usuarios/{id}` — perfil público sin auth

#### Frontend ✅
- [x] `frontend/pages/estudiante/perfil.html`
  - Avatar con inicial, badge de nivel de verificación
  - Barra de progreso de créditos (`creditos / 264`) con actualización en tiempo real
  - 3 secciones: datos académicos / datos personales / portafolio (GitHub + CV)
  - Guardado parcial con `api.updateMe()` + mensaje de confirmación
- [x] `frontend/pages/empresa/perfil.html`
  - Edición de nombre de empresa, sector, sitio web, nombre de contacto
- [x] `frontend/pages/referidor/perfil.html`
  - Edición de nombre y carrera de egresado

### Endpoints a usar

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/usuarios/me` | ✅ JWT | Mi perfil completo |
| PUT | `/api/usuarios/me` | ✅ JWT | Actualizar campos del perfil |
| GET | `/api/usuarios/{id}` | ❌ | Perfil público |

---

## Sprint 3 — Vacantes: Publicación, Feed y Filtros ✅ COMPLETO

**Objetivo:** El ciclo de publicación funciona de extremo a extremo.

### Resultado
> "La empresa TechGT publica 'Backend Junior' para Sistemas, semestre mínimo 6. El estudiante Ana filtra por Sistemas y ve las vacantes aprobadas. Hace clic en una vacante y ve el detalle completo."

### Entregado

#### Backend ✅ (ya estaba implementado)
- [x] `POST /api/vacantes/` — crea vacante en estado `pendiente`
- [x] `GET /api/vacantes/` — lista solo las `aprobadas`, con filtros
- [x] `GET /api/vacantes/{id}` — detalle de una vacante
- [x] `GET /api/vacantes/mis-vacantes/publicadas` — vacantes del publicador autenticado

#### Frontend ✅
- [x] `frontend/pages/empresa/publicar-vacante.html`
  - Autocompletado de empresa desde `api.getMe()`
  - Sección de exclusividad: checkbox `solo_plataforma` + datepicker condicional `exclusiva_hasta`
- [x] `frontend/pages/referidor/publicar-referido.html`
  - Estilo visual diferenciado (borde punteado, lavanda)
  - Campo de nota personal obligatoria + enlace oficial opcional
  - Autocompletado de carrera egresada desde perfil
- [x] `frontend/pages/estudiante/vacantes.html`
  - Feed con 4 filtros en tiempo real: carrera, semestre mínimo, tipo de contrato, tipo
  - Tarjetas diferenciadas empresa (blueprint) vs referido (dashed/lavanda)
  - Contador de resultados + empty state descriptivo
- [x] `frontend/pages/estudiante/vacante-detalle.html`
  - Carga por `?id=` desde URL
  - Muestra todos los campos, nota del referidor destacada
  - Barra de acción sticky (botón "Postular" — conectado en Sprint 4)
- [x] `frontend/pages/empresa/mis-vacantes.html`
  - Sirve para empresa Y referidor (detecta rol automáticamente)
  - Badge de estado con colores: pendiente / aprobada / rechazada
  - Nota de "en revisión" para las pendientes

### Endpoints a usar

| Método | Ruta | Auth | Notas |
|--------|------|------|-------|
| POST | `/api/vacantes/` | ✅ empresa/referidor | Body: `CrearVacante` |
| GET | `/api/vacantes/` | ❌ | `?carrera=&semestre_minimo=&tipo_contrato=&tipo=` |
| GET | `/api/vacantes/{id}` | ❌ | |
| GET | `/api/vacantes/mis-vacantes/publicadas` | ✅ empresa/referidor | |

#### Enums del backend
```
tipo_contrato: "tiempo_completo" | "medio_tiempo" | "practica" | "freelance"
modalidad:     "presencial" | "remoto" | "hibrido"
tipo:          "empresa" | "referido"
```

---

## Sprint 4 — Postulaciones + Moderación ✅ COMPLETO

**Objetivo:** El ciclo completo funciona: empresa publica → moderador aprueba → vacante aparece en feed → estudiante postula → empresa gestiona candidatos.

### Resultado
> "El moderador revisa la vacante de TechGT, la aprueba, y aparece en el feed. Ana la ve, hace clic en 'Postular', y queda registrada con estado 'Enviada'. TechGT cambia el estado a 'En revisión'."

### Entregado

#### Backend ✅ (implementado en este sprint + base ya existente)
- [x] `POST /api/postulaciones/` — crea postulación, requiere rol estudiante
  - Devuelve 400 si ya existe (`UniqueConstraint`)
  - Devuelve 404 si la vacante no está `aprobada`
- [x] `GET /api/postulaciones/mis-postulaciones` — postulaciones del estudiante
- [x] `GET /api/postulaciones/vacante/{vacante_id}` — **NUEVO:** candidatos por vacante (requiere empresa dueña)
- [x] `PUT /api/postulaciones/{id}/estado` — actualiza estado, solo empresa dueña
- [x] `GET /api/moderacion/cola` — vacantes `pendientes`, solo moderador
- [x] `GET /api/moderacion/historial` — últimas 50 `aprobadas` y `rechazadas`
- [x] `PUT /api/moderacion/vacantes/{id}` — aprobar o rechazar

#### Frontend ✅
- [x] `frontend/pages/estudiante/vacante-detalle.html` — botón "Postular" funcional
  - Maneja "Ya postulaste" sin duplicar, cambia UI tras éxito
- [x] `frontend/pages/estudiante/postulaciones.html`
  - Badges de color por estado (enviada/en_revision/aceptada/rechazada)
  - Enriquece cada postulación con datos de la vacante vía `api.getVacante()` en paralelo
  - Empty state con CTA a explorar vacantes
- [x] `frontend/pages/moderador/cola.html`
  - Lista de pendientes con botón "Revisar"
  - Diálogo con descripción completa; aprobar en 1 clic, rechazar pide motivo en 2 pasos
  - Toast de confirmación + recarga automática tras cada acción
- [x] `frontend/pages/moderador/historial.html`
  - Últimas 50 vacantes procesadas con badge aprobada/rechazada
- [x] `frontend/pages/empresa/candidatos.html`
  - Agrupa candidatos por vacante aprobada
  - Selector de estado inline + campo de nota por candidato
  - Carga perfiles y postulaciones en paralelo con `Promise.all`

### Ciclo completo de moderación
```
empresa publica vacante
  → estado: "pendiente"
  → NO aparece en feed del estudiante

moderador aprueba (PUT /api/moderacion/vacantes/{id})
  → estado: "aprobada"
  → APARECE en feed del estudiante

estudiante postula (POST /api/postulaciones/)
  → postulacion con estado: "enviada"

empresa revisa (PUT /api/postulaciones/{id}/estado)
  → estado: "en_revision" | "aceptada" | "rechazada"
```

### Endpoints del sprint

| Método | Ruta | Auth | Notas |
|--------|------|------|-------|
| POST | `/api/postulaciones/` | ✅ estudiante | `{vacante_id: int}` |
| GET | `/api/postulaciones/mis-postulaciones` | ✅ estudiante | |
| GET | `/api/postulaciones/vacante/{id}` | ✅ empresa | Nuevo — no estaba en spec original |
| PUT | `/api/postulaciones/{id}/estado` | ✅ empresa | `{estado, nota_empresa}` |
| GET | `/api/moderacion/cola` | ✅ moderador | |
| GET | `/api/moderacion/historial` | ✅ moderador | |
| PUT | `/api/moderacion/vacantes/{id}` | ✅ moderador | `{accion, motivo}` |

---

## Sprint 5 — Certificaciones + Nivel + Notificaciones ✅ COMPLETO

**Objetivo:** Sistema completo con los diferenciadores de negocio: verificación de nivel, certificaciones y notificaciones automáticas.

### Resultado
> "Ana sube una certificación de Python de Coursera. El moderador la verifica. Su nivel sube a 'certificado'. Cuando su postulación cambia de estado, recibe una notificación en el 🔔 de la navbar."

### Entregado

#### Backend ✅
- [x] `backend/app/schemas/certificacion.py` — `CrearCertificacion` + `CertificacionResponse`
- [x] `backend/app/routers/certificaciones.py`
  - `POST /api/certificaciones/` — estudiante registra certificación (estado inicial: `pendiente`)
  - `GET /api/certificaciones/mis-certificaciones` — lista del usuario autenticado
  - `GET /api/certificaciones/pendientes` — cola del moderador
  - `PUT /api/certificaciones/{id}/verificar` — moderador verifica + llama `recalcular_nivel()`
  - `PUT /api/certificaciones/{id}/rechazar` — moderador rechaza
- [x] `recalcular_nivel()` — lógica de nivel automático tras verificar:
  ```python
  0 certs verificadas → basico
  1-2 certs verificadas → certificado
  3+ certs verificadas → verificado
  ```
- [x] `routers/moderacion.py` — notificaciones automáticas al aprobar/rechazar vacante
  - Al aprobar: notifica a todos los estudiantes con carrera + semestre compatibles
  - Al aprobar: notifica al publicador ("tu vacante fue aprobada")
  - Al rechazar: notifica al publicador con el motivo
- [x] `routers/postulaciones.py` — notificación automática al cambiar estado de postulación
- [x] `main.py` — registra el router de certificaciones en `/api/certificaciones`

#### Frontend ✅
- [x] `frontend/js/api.js` — 5 nuevos métodos: `agregarCertificacion`, `misCertificaciones`, `certsPendientes`, `verificarCert`, `rechazarCert`
- [x] `frontend/js/notif.js` — módulo de badge de notificaciones
  - Inyecta campana 🔔 con badge numérico en el nav
  - Dropdown con últimas 10 notificaciones
  - Marcar como leída al hacer hover
  - Refresca automáticamente cada 30 segundos
- [x] `frontend/pages/estudiante/perfil.html` — sección de certificaciones
  - Lista con badge de estado (en revisión / verificada / rechazada)
  - Formulario desplegable para agregar nueva certificación
- [x] `frontend/pages/moderador/certificaciones.html`
  - Lista de certs pendientes con link de verificación
  - Botones verificar / rechazar con confirmación
  - Toast + recarga automática
- [x] `frontend/pages/moderador/home.html`
  - Tercer stat card: "Certs. pendientes" con contador en vivo
  - Link a la nueva página de certificaciones
- [x] `frontend/pages/estudiante/home.html` — badge de notificaciones activo
- [x] `frontend/pages/empresa/home.html` — badge de notificaciones activo

### Jerarquía de niveles de verificación
```
pendiente  → cuenta creada, sin acciones
basico     → sin certificaciones verificadas (pero perfil activo)
certificado → 1-2 certificaciones verificadas
verificado  → 3+ certificaciones verificadas
```

### Endpoints del sprint

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/api/certificaciones/` | ✅ estudiante | Registrar certificación |
| GET | `/api/certificaciones/mis-certificaciones` | ✅ estudiante | Lista propias |
| GET | `/api/certificaciones/pendientes` | ✅ moderador | Cola de verificación |
| PUT | `/api/certificaciones/{id}/verificar` | ✅ moderador | Verifica + recalcula nivel |
| PUT | `/api/certificaciones/{id}/rechazar` | ✅ moderador | Rechaza |
| GET | `/api/notificaciones/` | ✅ cualquier rol | Lista (máx 50) |
| PUT | `/api/notificaciones/{id}/leer` | ✅ | Marcar leída |
| PUT | `/api/notificaciones/leer-todas` | ✅ | Marcar todas leídas |

---

## Referencia rápida de archivos por sprint

| Sprint | Backend | Frontend |
|--------|---------|----------|
| 1 | ✅ auth, modelos, seed | ✅ index, login, api.js, auth.js, registro x3, dashboards x4 |
| 2 | ✅ ya implementado | ✅ perfil.html x3 roles |
| 3 | ✅ ya implementado | ✅ publicar-vacante, publicar-referido, vacantes, vacante-detalle, mis-vacantes |
| 4 | ✅ + nuevo endpoint postulaciones/vacante | ✅ postulaciones, cola, historial, candidatos, botón postular |
| 5 | ✅ certificaciones router + notif automáticas | ✅ notif.js, certs en perfil, moderador/certificaciones, badge 🔔 |

---

## Checklist final — Estado actual

- [x] La app corre con `python run.py` desde `backend/`
- [x] `python seed.py` crea datos de prueba sin errores
- [x] Los 4 flujos completos funcionan: estudiante, empresa, referidor, moderador
- [x] El ciclo completo publicar → moderar → postular → actualizar estado funciona
- [x] Sistema de certificaciones y niveles implementado
- [x] Notificaciones automáticas en aprobación de vacantes y cambios de estado
- [x] No hay datos hardcodeados en el frontend (todo viene del API)
- [x] El `.env` no está en git (solo `env.example`)
- [x] La BD `.db` no está en git
- [x] Cada página protegida llama a `auth.requireAuth(["rol"])` al cargar
- [x] La API devuelve errores descriptivos (no solo 500 genéricos)
