# Plan de Desarrollo — Plataforma de Empleo USAC

> **5 sprints autoconclusivos** — cada uno entrega un slice vertical funcional y desplegable. Al terminar cada sprint, la aplicación corre y es demostrable. Los sprints están diseñados para que 3-5 personas trabajen en paralelo sin pisarse.

---

## Arquitectura general

```
┌─────────────────────────────────────────────────┐
│  Frontend (HTML + JS vanilla + Industry DS)      │
│  http://localhost:8000/                          │
│                                                  │
│  js/api.js  ──►  fetch("/api/...")               │
│  js/auth.js ──►  localStorage JWT + guards       │
└──────────────────────┬──────────────────────────┘
                       │ HTTP / REST
┌──────────────────────▼──────────────────────────┐
│  Backend (FastAPI · Python 3.11)                 │
│  http://localhost:8000/api/...                   │
│  Swagger: http://localhost:8000/api/docs         │
│                                                  │
│  routers/auth.py         /api/auth/*             │
│  routers/usuarios.py     /api/usuarios/*         │
│  routers/vacantes.py     /api/vacantes/*         │
│  routers/postulaciones.py /api/postulaciones/*   │
│  routers/moderacion.py   /api/moderacion/*       │
│  routers/notificaciones.py /api/notificaciones/* │
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

## Sprint 1 — Fundación: Backend + Auth + Estructura

**Duración estimada:** 1 semana  
**Objetivo:** El proyecto corre localmente. Cualquier miembro del equipo puede registrarse y hacer login. La estructura de carpetas está definida y todos trabajan sobre la misma base.

### Resultado al final del sprint
> "Abrimos `http://localhost:8000`, nos registramos como estudiante, el sistema nos devuelve un JWT, y hacemos login con esas credenciales. La página de inicio carga con el design system."

### Estado de partida (ya está hecho)
- ✅ Estructura de carpetas creada
- ✅ `backend/app/models/` — todos los modelos SQLAlchemy
- ✅ `backend/app/schemas/auth.py` — schemas de registro/login
- ✅ `backend/app/routers/auth.py` — endpoints `/api/auth/registro` y `/api/auth/login`
- ✅ `backend/app/core/security.py` — hashing bcrypt + JWT
- ✅ `backend/app/core/deps.py` — `get_current_user`, `require_role`
- ✅ `backend/app/main.py` — app FastAPI con rutas y static files
- ✅ `backend/seed.py` — datos de prueba
- ✅ `frontend/index.html` — landing con selector de rol
- ✅ `frontend/login.html` — formulario de login funcional
- ✅ `frontend/js/api.js` — cliente HTTP
- ✅ `frontend/js/auth.js` — JWT storage + guards

### Tareas del sprint (lo que FALTA)

#### Backend (persona A)
- [ ] Crear y activar el entorno virtual, instalar `requirements.txt`
- [ ] Copiar `env.example` → `.env`
- [ ] Ejecutar `python seed.py` y verificar que crea la BD sin errores
- [ ] Verificar Swagger en http://localhost:8000/api/docs
- [ ] Probar manualmente los endpoints de auth con Swagger o curl:
  ```bash
  curl -X POST http://localhost:8000/api/auth/registro \
    -H "Content-Type: application/json" \
    -d '{"email":"test@usac.edu.gt","password":"test123","tipo_usuario":"estudiante","nombre":"Test"}'
  ```

#### Frontend — Registro estudiante (persona B)
- [ ] Crear `frontend/pages/registro/estudiante.html`
  - Formulario multi-step: (1) cuenta, (2) datos personales, (3) datos académicos
  - Campos: email, password, nombre, teléfono, carrera, escuela, semestre, créditos, estado académico
  - Al enviar: `api.registro({email, password, tipo_usuario: "estudiante", nombre})`
  - Guardar sesión con `auth.saveSession(response)` y redirigir a `/pages/estudiante/home.html`
  - Usar clases del Industry DS: `.field`, `.input`, `.btn`, `.card.blueprint`

#### Frontend — Registro empresa y referidor (persona C)
- [ ] Crear `frontend/pages/registro/empresa.html`
  - Campos: nombre de empresa, correo de contacto, sector, sitio web
  - Mapeo: `tipo_usuario: "empresa"`, `nombre: nombreEmpresa`
- [ ] Crear `frontend/pages/registro/referidor.html`
  - Campos: nombre completo, correo, carrera de la que egresó
  - Mapeo: `tipo_usuario: "referidor"`

#### Frontend — Dashboards placeholder (persona D)
- [ ] Crear `frontend/pages/estudiante/home.html` — stub con navbar y mensaje de bienvenida
- [ ] Crear `frontend/pages/empresa/home.html` — stub
- [ ] Crear `frontend/pages/referidor/home.html` — stub
- [ ] Crear `frontend/pages/moderador/home.html` — stub
- [ ] Cada dashboard debe llamar `auth.requireAuth(["rol"])` al cargar para proteger la ruta

### Especificaciones técnicas

#### Endpoints disponibles al inicio del sprint

| Método | Ruta | Body | Respuesta |
|--------|------|------|-----------|
| POST | `/api/auth/registro` | `{email, password, tipo_usuario, nombre}` | `{access_token, tipo_usuario, user_id, nombre}` |
| POST | `/api/auth/login` | `{email, password}` | `{access_token, tipo_usuario, user_id, nombre}` |

#### Guard de ruta (patrón para TODOS los dashboards)
```javascript
// Al inicio del <script type="module"> de cada página protegida:
import { auth } from "/js/auth.js";
const user = auth.requireAuth(["estudiante"]); // o ["empresa"], ["moderador"], etc.
document.getElementById("userName").textContent = user.nombre;
```

### Criterios de aceptación
- [ ] `python run.py` arranca sin errores con la BD vacía
- [ ] `python seed.py` crea 4 usuarios y 3 vacantes sin errores
- [ ] POST `/api/auth/registro` con email nuevo → devuelve JWT
- [ ] POST `/api/auth/registro` con email duplicado → devuelve 400
- [ ] POST `/api/auth/login` con credenciales correctas → devuelve JWT
- [ ] POST `/api/auth/login` con contraseña incorrecta → devuelve 401
- [ ] Abrir http://localhost:8000 → carga `index.html` con design system
- [ ] Hacer clic en "Estudiante" → carga formulario de registro
- [ ] Completar registro → redirige a `home.html` del estudiante
- [ ] Abrir `home.html` directamente sin token → redirige a `/login.html`

### División sugerida (4 personas)
| Persona | Tarea |
|---------|-------|
| A | Setup backend + verificación endpoints |
| B | Registro estudiante (HTML + JS) |
| C | Registro empresa + referidor |
| D | Dashboards placeholder (4 páginas) |

---

## Sprint 2 — Perfiles de Usuario + Dashboards por Rol

**Duración estimada:** 1 semana  
**Objetivo:** Cada usuario puede ver y editar su perfil completo. Los dashboards de cada rol muestran información real del usuario y tienen navegación funcional. El login diferencia primer acceso de accesos posteriores.

### Resultado al final del sprint
> "El estudiante Ana entra a su perfil, completa su carrera, semestre y bio, y la barra de créditos muestra su progreso. La empresa ve su nombre y sector. El referidor ve su carrera egresada."

### Tareas del sprint

#### Backend (persona A)
Todos los endpoints de usuarios **ya están implementados** en `routers/usuarios.py`. Solo verificar que funcionan:
- [ ] `GET /api/usuarios/me` — requiere JWT, devuelve perfil completo
- [ ] `PUT /api/usuarios/me` — actualiza campos del perfil (solo los enviados, el resto no se toca)
- [ ] `GET /api/usuarios/{id}` — perfil público, sin auth
- [ ] Probar con Swagger que los campos opcionales del modelo se actualizan correctamente

#### Frontend — Perfil del estudiante (persona B)
- [ ] Crear `frontend/pages/estudiante/perfil.html`
  - Al cargar: `const perfil = await api.getMe()`
  - Mostrar: nombre, email, carrera, escuela, semestre, créditos, estado académico, bio, URLs
  - **Barra de progreso de créditos:** `(creditos_aprobados / 264) * 100`%
    ```html
    <div style="height:4px; background:var(--color-neutral-200); border-radius:2px;">
      <div id="barraCreditos" style="height:100%; background:var(--color-accent); border-radius:2px;"></div>
    </div>
    ```
  - Formulario de edición inline o modal (usar `.dialog` del design system)
  - Al guardar: `await api.updateMe({carrera, semestre, ...})`

#### Frontend — Dashboard estudiante (persona B)
- [ ] Actualizar `frontend/pages/estudiante/home.html`
  - Mostrar nombre del usuario (`user.nombre`)
  - 3 acciones rápidas: "Ver vacantes" / "Mi perfil" / "Mis postulaciones"
  - Badge de nivel de verificación (`nivel_verificacion`)
  - Sección de notificaciones (stub — se llena en Sprint 5)

#### Frontend — Perfil y dashboard empresa (persona C)
- [ ] Crear `frontend/pages/empresa/perfil.html`
  - Campos editables: nombre empresa, sector, sitio web, nombre de contacto, teléfono
  - Actualizar con `api.updateMe({nombre_empresa, sector, sitio_web, ...})`
- [ ] Actualizar `frontend/pages/empresa/home.html`
  - Mostrar nombre de empresa
  - 3 acciones: "Publicar vacante" / "Mis vacantes" / "Mi perfil"

#### Frontend — Perfil y dashboard referidor y moderador (persona D)
- [ ] Crear `frontend/pages/referidor/perfil.html`
  - Campos: nombre, carrera egresada, correo
- [ ] Actualizar `frontend/pages/referidor/home.html`
- [ ] Actualizar `frontend/pages/moderador/home.html`
  - Acciones: "Cola de verificación" / "Historial"

### Especificaciones técnicas

#### Endpoints a usar en este sprint

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/usuarios/me` | ✅ JWT | Mi perfil completo |
| PUT | `/api/usuarios/me` | ✅ JWT | Actualizar campos del perfil |
| GET | `/api/usuarios/{id}` | ❌ | Perfil público |

#### Patrón de carga de perfil
```javascript
import { api } from "/js/api.js";
import { auth } from "/js/auth.js";

const user = auth.requireAuth(["estudiante"]);
const perfil = await api.getMe();

document.getElementById("nombre").textContent = perfil.nombre;
document.getElementById("carrera").textContent = perfil.carrera ?? "Sin carrera";
// ...
```

#### Patrón de edición de perfil
```javascript
document.getElementById("guardarBtn").addEventListener("click", async () => {
  try {
    await api.updateMe({
      carrera: document.getElementById("carreraInput").value,
      semestre: Number(document.getElementById("semestreInput").value),
    });
    alert("Perfil actualizado");
  } catch (err) {
    alert("Error: " + err.message);
  }
});
```

### Criterios de aceptación
- [ ] `GET /api/usuarios/me` con JWT válido → devuelve todos los campos del perfil
- [ ] `PUT /api/usuarios/me` con `{semestre: 7}` → solo actualiza semestre, no toca el resto
- [ ] Página de perfil del estudiante carga con los datos del usuario autenticado
- [ ] Editar carrera y guardar → los datos persisten en SQLite (verificar recargando)
- [ ] Barra de créditos refleja el porcentaje correcto (`creditos / 264`)
- [ ] `GET /api/usuarios/5` (sin auth) → devuelve datos públicos del usuario 5
- [ ] Dashboard de cada rol muestra el nombre del usuario real, no hardcodeado

---

## Sprint 3 — Vacantes: Publicación, Feed y Filtros

**Duración estimada:** 1-2 semanas  
**Objetivo:** El ciclo de publicación funciona de extremo a extremo. Empresa y referidor publican vacantes. El estudiante ve un feed filtrado. Las vacantes recién publicadas entran en estado `pendiente` (no visibles hasta aprobación del Sprint 4).

### Resultado al final del sprint
> "La empresa TechGT publica 'Backend Junior' para Sistemas, semestre mínimo 6. El estudiante Ana filtra por Sistemas y ve las vacantes aprobadas. Hace clic en una vacante y ve el detalle completo."

### Tareas del sprint

#### Backend (persona A)
Todos los endpoints de vacantes **ya están implementados** en `routers/vacantes.py`. Verificar:
- [ ] `POST /api/vacantes/` — crea vacante en estado `pendiente`
- [ ] `GET /api/vacantes/` — lista solo las `aprobadas`, con filtros por query params
- [ ] `GET /api/vacantes/{id}` — detalle de una vacante
- [ ] `GET /api/vacantes/mis-vacantes/publicadas` — vacantes de la empresa/referidor autenticado
- [ ] Verificar que el filtro `semestre_minimo` es `<=` (una vacante con mínimo 5 aparece al buscar semestre 7)
- [ ] Verificar que `solo_plataforma=true` en una vacante no la excluye del feed para usuarios autenticados (nota: la lógica de exclusividad completa va en Sprint 5)

#### Frontend — Formulario publicar vacante (empresa) (persona B)
- [ ] Crear `frontend/pages/empresa/publicar-vacante.html`
  - Campos: puesto, nombre empresa (autocompletado del perfil), carrera compatible, semestre mínimo, modalidad (select), tipo contrato (select), ubicación, descripción, requisitos
  - Campo exclusividad: checkbox "Solo disponible en plataforma" + datepicker "Exclusiva hasta"
  - Al enviar: `api.publicarVacante({tipo: "empresa", puesto, empresa_nombre, ...})`
  - Redirigir a `mis-vacantes.html` o mostrar confirmación
  - Agregar link "Publicar vacante" al dashboard de empresa

#### Frontend — Formulario publicar referido (referidor) (persona B)
- [ ] Crear `frontend/pages/referidor/publicar-referido.html`
  - Mismos campos base + nota personal (textarea) + enlace oficial (opcional)
  - `tipo: "referido"` en el body
  - Mostrar diferencia visual: "Tu nota personal aparecerá en la tarjeta de la vacante"

#### Frontend — Feed de vacantes (persona C)
- [ ] Crear `frontend/pages/estudiante/vacantes.html`
  - Al cargar: `const vacantes = await api.getVacantes()`
  - Filtros en tiempo real (sin recarga de página):
    - Select "Carrera" → `api.getVacantes({carrera})`
    - Select "Semestre mínimo" → `api.getVacantes({semestre_minimo})`
    - Select "Tipo contrato" → `api.getVacantes({tipo_contrato})`
  - Contador: "X vacantes disponibles"
  - Renderizar tarjetas diferenciadas (empresa vs. referido):

  ```javascript
  function renderTarjeta(vacante) {
    const esReferido = vacante.tipo === "referido";
    return `
      <div class="card ${esReferido ? '' : 'blueprint'}" style="${esReferido ? 'border:1px dashed var(--color-accent-2); background:...' : ''}">
        ${!esReferido ? '<i class="corner tl"></i><i class="corner tr"></i><i class="corner bl"></i><i class="corner br"></i>' : ''}
        <span class="tag ${esReferido ? 'tag-accent-2' : 'tag-accent'}">${esReferido ? 'Referido por ' + vacante.publicador_id : 'Empresa'}</span>
        <div class="card-title">${vacante.puesto}</div>
        <div class="card-body">${vacante.empresa_nombre} · ${vacante.ubicacion ?? ''}</div>
        <div style="display:flex; gap:6px; flex-wrap:wrap;">
          <span class="tag tag-neutral">${vacante.tipo_contrato}</span>
          <span class="tag tag-neutral">${vacante.modalidad}</span>
          <span class="tag tag-neutral">Desde sem. ${vacante.semestre_minimo}</span>
        </div>
        ${esReferido && vacante.nota_personal ? `<p style="font-style:italic; font-size:13px;">"${vacante.nota_personal}"</p>` : ''}
        <a href="/pages/estudiante/vacante-detalle.html?id=${vacante.id}" class="btn btn-secondary" style="margin-top:8px;">Ver detalle</a>
      </div>
    `;
  }
  ```

#### Frontend — Detalle de vacante (persona C)
- [ ] Crear `frontend/pages/estudiante/vacante-detalle.html`
  - Leer `id` de la URL: `new URLSearchParams(location.search).get("id")`
  - Cargar: `const vacante = await api.getVacante(id)`
  - Mostrar todos los campos, incluyendo nota personal si es referido
  - Botón "Postular" (se conecta en Sprint 4)

#### Frontend — Mis vacantes (empresa/referidor) (persona D)
- [ ] Crear `frontend/pages/empresa/mis-vacantes.html` (y equivalente para referidor)
  - `const vacantes = await api.misVacantes()`
  - Mostrar estado de cada vacante: badge `pendiente / aprobada / rechazada`
  - Estado `pendiente` con nota: "Esta vacante está en revisión por el moderador"

### Especificaciones técnicas

#### Endpoints a usar en este sprint

| Método | Ruta | Auth | Notas |
|--------|------|------|-------|
| POST | `/api/vacantes/` | ✅ empresa/referidor | Body: `CrearVacante` |
| GET | `/api/vacantes/` | ❌ | ?carrera=&semestre_minimo=&tipo_contrato=&tipo= |
| GET | `/api/vacantes/{id}` | ❌ | |
| GET | `/api/vacantes/mis-vacantes/publicadas` | ✅ empresa/referidor | |

#### Tipos de contrato y modalidad (enums del backend)
```
tipo_contrato: "tiempo_completo" | "medio_tiempo" | "practica" | "freelance"
modalidad:     "presencial" | "remoto" | "hibrido"
tipo:          "empresa" | "referido"
```

### Criterios de aceptación
- [ ] Empresa publica vacante → aparece en sus "mis vacantes" con estado `pendiente`
- [ ] Vacante `pendiente` NO aparece en el feed del estudiante
- [ ] Feed muestra solo vacantes `aprobadas`
- [ ] Filtro por carrera filtra correctamente (case-insensitive)
- [ ] Filtro por semestre mínimo: estudiante con semestre 7 ve vacantes con mínimo ≤ 7
- [ ] Tarjeta de empresa y tarjeta de referido se ven visualmente distintas
- [ ] Clic en "Ver detalle" → carga detalle de esa vacante específica
- [ ] Sin filtros activos, el contador muestra el total de vacantes aprobadas

---

## Sprint 4 — Postulaciones + Moderación

**Duración estimada:** 1-2 semanas  
**Objetivo:** El ciclo completo funciona: empresa publica → moderador aprueba → vacante aparece en feed → estudiante postula → empresa gestiona candidatos.

### Resultado al final del sprint
> "El moderador revisa la vacante de TechGT, la aprueba, y aparece en el feed. Ana la ve, hace clic en 'Postular', y queda registrada con estado 'Enviada'. TechGT cambia el estado a 'En revisión'."

### Tareas del sprint

#### Backend (persona A)
Todos los endpoints de postulaciones y moderación **ya están implementados**. Verificar y testear:
- [ ] `POST /api/postulaciones/` — crea postulación, requiere rol estudiante
  - Devuelve 400 si ya existe una postulación de ese estudiante a esa vacante (`UniqueConstraint`)
  - Devuelve 404 si la vacante no existe o no está `aprobada`
- [ ] `GET /api/postulaciones/mis-postulaciones` — lista postulaciones del estudiante autenticado
- [ ] `PUT /api/postulaciones/{id}/estado` — actualiza estado, solo la empresa dueña de la vacante
- [ ] `GET /api/moderacion/cola` — lista vacantes `pendientes`, solo moderador
- [ ] `GET /api/moderacion/historial` — lista `aprobadas` y `rechazadas`, solo moderador
- [ ] `PUT /api/moderacion/vacantes/{id}` — aprobar o rechazar, body `{accion: "aprobar"|"rechazar", motivo: ""}`

#### Frontend — Flujo de postulación (persona B)
- [ ] Actualizar `frontend/pages/estudiante/vacante-detalle.html`
  - Botón "Postular a esta vacante" → `api.postular(vacante.id)`
  - Manejo de error: si ya postulaste → mostrar "Ya aplicaste a esta vacante" (estado 400)
  - Después de postular: cambiar botón a "Postulación enviada ✓"
- [ ] Crear `frontend/pages/estudiante/postulaciones.html`
  - `const postulaciones = await api.misPostulaciones()`
  - Mostrar cada postulación con el nombre del puesto y el estado actual
  - Badge de estado con color por estado:
    - `enviada` → tag-neutral (gris)
    - `en_revision` → tag-accent-2 (lavanda)
    - `aceptada` → tag-accent (azul)
    - `rechazada` → rojo/neutro opaco
  - Estado vacío: "Aún no te has postulado a ninguna vacante"

#### Frontend — Panel de moderación (persona C)
- [ ] Crear `frontend/pages/moderador/cola.html`
  - Al cargar: `const cola = await api.getCola()`
  - Lista de vacantes pendientes con: puesto, empresa, carrera, fecha de publicación
  - Botón "Revisar" en cada vacante → abre diálogo (usar `.dialog` del design system):
    ```html
    <div class="dialog-backdrop" id="backdrop">
      <div class="dialog blueprint">
        <i class="corner tl"></i><i class="corner tr"></i>
        <i class="corner bl"></i><i class="corner br"></i>
        <div class="dialog-title" id="dialogPuesto"></div>
        <div class="dialog-body" id="dialogDescripcion"></div>
        <div class="dialog-actions">
          <button class="btn btn-ghost" id="rechazarBtn">Rechazar</button>
          <button class="btn btn-primary" id="aprobarBtn">Aprobar</button>
        </div>
      </div>
    </div>
    ```
  - Al aprobar: `api.moderarVacante(id, {accion: "aprobar"})` → remover de lista, mostrar toast
  - Al rechazar: pedir motivo → `api.moderarVacante(id, {accion: "rechazar", motivo})`
- [ ] Actualizar `frontend/pages/moderador/home.html`
  - Mostrar contador de vacantes en cola

#### Frontend — Candidatos para empresa (persona D)
- [ ] Crear `frontend/pages/empresa/candidatos.html`
  - Por vacante publicada por la empresa, mostrar las postulaciones recibidas
  - Para cada postulación: nombre del estudiante (`api.getPerfil(estudiante_id)`), carrera, semestre, estado
  - Selector de estado: dropdown para cambiar a `en_revision / aceptada / rechazada`
  - Al cambiar: `api.actualizarEstado(postulacion.id, {estado: nuevoEstado})`

### Especificaciones técnicas

#### Endpoints a usar en este sprint

| Método | Ruta | Auth | Notas |
|--------|------|------|-------|
| POST | `/api/postulaciones/` | ✅ estudiante | `{vacante_id: int}` |
| GET | `/api/postulaciones/mis-postulaciones` | ✅ estudiante | |
| PUT | `/api/postulaciones/{id}/estado` | ✅ empresa | `{estado, nota_empresa}` |
| GET | `/api/moderacion/cola` | ✅ moderador | |
| GET | `/api/moderacion/historial` | ✅ moderador | |
| PUT | `/api/moderacion/vacantes/{id}` | ✅ moderador | `{accion, motivo}` |

#### Ciclo completo de moderación
```
empresa publica vacante
  → estado: "pendiente"
  → NO aparece en feed del estudiante

moderador aprueba (PUT /api/moderacion/vacantes/{id} con accion:"aprobar")
  → estado: "aprobada"
  → APARECE en feed del estudiante

estudiante postula (POST /api/postulaciones/)
  → se crea postulacion con estado: "enviada"

empresa revisa (PUT /api/postulaciones/{id}/estado)
  → estado: "en_revision" | "aceptada" | "rechazada"
```

### Criterios de aceptación
- [ ] Moderador ve solo vacantes en estado `pendiente` en la cola
- [ ] Al aprobar → vacante cambia a `aprobada`, desaparece de la cola, aparece en el feed
- [ ] Al rechazar → vacante cambia a `rechazada`, desaparece de la cola
- [ ] Estudiante puede postularse a vacante `aprobada`
- [ ] Postularse dos veces a la misma vacante → error "Ya postulaste" (no duplicado en BD)
- [ ] Estudiante sin token no puede postularse (401)
- [ ] Empresa cambia estado de postulación → cambio persiste en BD
- [ ] Empresa solo puede cambiar estado de postulaciones a SUS vacantes (403 si intenta con otra)
- [ ] "Mis postulaciones" del estudiante muestra el estado actualizado por la empresa

---

## Sprint 5 — Certificaciones + Nivel + Notificaciones + Pulido

**Duración estimada:** 1-2 semanas  
**Objetivo:** Sistema completo con los diferenciadores de negocio — verificación de nivel de usuario, certificaciones, y notificaciones. Además: estados de error/carga, sistema de reputación básico, y pulido general.

### Resultado al final del sprint
> "Ana sube una certificación de Python de Coursera. El moderador la verifica. Su nivel sube a 'básico'. Una vacante exclusiva requiere nivel 'certificado' y Ana no puede verla. Cuando su vacante cambia de estado, recibe una notificación en la navbar."

### Tareas del sprint

#### Backend — Certificaciones (persona A)
Los endpoints de certificaciones **no están implementados** — crearlos en `routers/certificaciones.py`:
- [ ] `POST /api/certificaciones/` — estudiante registra certificación
  - Body: `{tipo, nombre, entidad_emisora, fecha_obtencion, url_verificacion}`
  - Estado inicial: `pendiente`
- [ ] `GET /api/certificaciones/mis-certificaciones` — lista del usuario autenticado
- [ ] `PUT /api/certificaciones/{id}/verificar` — solo moderador, cambia estado a `verificada`
  - Al verificar: evaluar si el usuario sube de nivel (lógica de nivel — ver abajo)
- [ ] Schema en `schemas/certificacion.py`

#### Backend — Lógica de nivel de usuario (persona A)
Agregar función en `routers/certificaciones.py` (o `core/nivel.py`):
```python
def recalcular_nivel(usuario: Usuario, db: Session):
    certs_verificadas = db.query(Certificacion).filter(
        Certificacion.usuario_id == usuario.id,
        Certificacion.estado == EstadoCertificacion.verificada,
    ).count()

    if certs_verificadas >= 3:
        usuario.nivel_verificacion = NivelVerificacion.verificado
    elif certs_verificadas >= 1:
        usuario.nivel_verificacion = NivelVerificacion.certificado
    else:
        usuario.nivel_verificacion = NivelVerificacion.basico
    db.commit()
```
- [ ] Llamar esta función después de verificar una certificación
- [ ] Aplicar filtro de nivel en `GET /api/vacantes/`: si una vacante tiene `nivel_minimo_requerido != "pendiente"`, solo mostrarla si el usuario autenticado tiene nivel suficiente (para usuarios no autenticados, no mostrar vacantes exclusivas de nivel alto)

#### Backend — Notificaciones automáticas (persona B)
Los endpoints de notificaciones ya están en `routers/notificaciones.py`. Implementar la **creación automática**:
- [ ] En `routers/moderacion.py`, al aprobar una vacante: crear notificaciones para todos los estudiantes cuya carrera coincide con `carrera_compatible` de la vacante
  ```python
  estudiantes_compatibles = db.query(Usuario).filter(
      Usuario.tipo_usuario == TipoUsuario.estudiante,
      Usuario.carrera == vacante.carrera_compatible,
      Usuario.semestre >= vacante.semestre_minimo,
  ).all()
  for estudiante in estudiantes_compatibles:
      db.add(Notificacion(
          usuario_id=estudiante.id,
          tipo=TipoNotificacion.vacante_compatible,
          titulo=f"Nueva vacante: {vacante.puesto}",
          mensaje=f"{vacante.empresa_nombre} publicó una vacante compatible con tu carrera.",
          referencia_id=vacante.id,
      ))
  ```
- [ ] En `routers/postulaciones.py`, al actualizar estado: crear notificación para el estudiante
  ```python
  db.add(Notificacion(
      usuario_id=postulacion.estudiante_id,
      tipo=TipoNotificacion.cambio_estado_postulacion,
      titulo=f"Tu postulación fue actualizada",
      mensaje=f"Tu postulación a '{postulacion.vacante.puesto}' cambió a: {nuevo_estado}",
      referencia_id=postulacion.id,
  ))
  ```

#### Frontend — Certificaciones en perfil del estudiante (persona C)
- [ ] Agregar sección de certificaciones a `frontend/pages/estudiante/perfil.html`
  - Lista de certificaciones: nombre, entidad, fecha, estado
  - Formulario para agregar nueva: `api.agregarCertificacion({...})`
  - Mostrar badge de nivel de verificación junto al nombre del usuario
- [ ] En panel del moderador, agregar sección "Certificaciones pendientes" con botón verificar

#### Frontend — Notificaciones en navbar (persona C)
- [ ] Crear componente navbar reutilizable `frontend/components/navbar.html`
  - Badge con conteo de notificaciones no leídas
  - Dropdown con lista de notificaciones recientes
  - Implementar en todas las páginas de cada rol
  ```javascript
  const notifs = await api.getNotificaciones();
  const noLeidas = notifs.filter(n => !n.leida).length;
  document.getElementById("notifBadge").textContent = noLeidas || "";
  ```

#### Frontend — Estados de error y carga (persona D)
- [ ] Crear `frontend/components/loader.html` — spinner mientras carga
- [ ] Agregar manejo de error global en `js/api.js`: mostrar toast en errores inesperados
- [ ] Agregar empty states a:
  - Feed sin resultados: "No encontramos vacantes con esos filtros"
  - Mis postulaciones vacías: "Aún no te has postulado a ninguna vacante"
  - Cola de moderación vacía: "No hay vacantes pendientes de revisión ✓"
- [ ] Agregar estado de carga mientras se hacen peticiones al API (deshabilitar botones + spinner)

#### Frontend — Reputación básica (persona D)
- [ ] Agregar campo de calificación en el modal de cambio de estado de empresa
  - "¿Qué tal fue el proceso con este candidato?" — 1 a 5 estrellas (solo si estado es `aceptada` o `rechazada`)
- [ ] Mostrar rating promedio en perfil público del estudiante

### Especificaciones técnicas

#### Endpoints nuevos a crear en este sprint

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/api/certificaciones/` | ✅ estudiante | Registrar certificación |
| GET | `/api/certificaciones/mis-certificaciones` | ✅ estudiante | Lista propias |
| PUT | `/api/certificaciones/{id}/verificar` | ✅ moderador | Verificar certificación |
| GET | `/api/notificaciones/` | ✅ cualquier rol | Lista notificaciones |
| PUT | `/api/notificaciones/{id}/leer` | ✅ | Marcar leída |
| PUT | `/api/notificaciones/leer-todas` | ✅ | Marcar todas leídas |

#### Jerarquía de niveles de verificación
```
pendiente  → cuenta creada, sin certificaciones verificadas
basico     → al completar perfil (carrera, semestre, bio, CV, GitHub)
certificado → 1+ certificaciones verificadas
verificado  → 3+ certificaciones verificadas
```

### Criterios de aceptación
- [ ] Estudiante agrega certificación → aparece con estado `pendiente`
- [ ] Moderador verifica certificación → estado cambia a `verificada`
- [ ] Al verificar la 1ra certificación → nivel del usuario sube a `certificado`
- [ ] Vacante con `nivel_minimo_requerido: "certificado"` NO aparece para usuarios con nivel `basico`
- [ ] Al aprobar vacante → estudiantes compatibles reciben notificación
- [ ] Al cambiar estado de postulación → estudiante recibe notificación
- [ ] Badge de notificaciones en navbar muestra conteo correcto
- [ ] Marcar como leída → badge decremente
- [ ] Feed sin resultados muestra mensaje útil, no pantalla en blanco
- [ ] Botones se deshabilitan durante peticiones al API (no double-submit)

---

## Checklist final antes de entregar

- [ ] La app corre con `python run.py` desde `backend/` desde un clon limpio del repo
- [ ] `python seed.py` crea datos de prueba sin errores
- [ ] Los 4 flujos completos funcionan: estudiante, empresa, referidor, moderador
- [ ] El ciclo completo publicar → moderar → postular → actualizar estado funciona
- [ ] No hay datos hardcodeados en el frontend (todo viene del API)
- [ ] El `.env` no está en git (solo `env.example`)
- [ ] La BD `.db` no está en git
- [ ] El `README.md` tiene instrucciones de setup que funcionan en una máquina nueva
- [ ] Cada página protegida llama a `auth.requireAuth(["rol"])` al cargar
- [ ] La API devuelve errores descriptivos (no solo 500 genéricos)

---

## Referencia rápida de archivos por sprint

| Sprint | Backend | Frontend |
|--------|---------|----------|
| 1 | ✅ Ya implementado | registro/estudiante.html, empresa.html, referidor.html + dashboards stub |
| 2 | ✅ Ya implementado | perfil.html (estudiante, empresa, referidor) + dashboards reales |
| 3 | ✅ Ya implementado | publicar-vacante.html, publicar-referido.html, vacantes.html, vacante-detalle.html, mis-vacantes.html |
| 4 | ✅ Ya implementado | postulaciones.html, cola.html, candidatos.html |
| 5 | routers/certificaciones.py + notif automáticas | perfil + certificaciones, navbar con badge, empty states |
