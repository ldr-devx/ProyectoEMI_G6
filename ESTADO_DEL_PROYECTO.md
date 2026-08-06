# Plataforma de Empleo Universitaria (USAC) — Estado del proyecto

**Archivo del prototipo:** `Plataforma Empleo USAC.dc.html`
**Última actualización:** modo oscuro + paleta fría (lavanda → azul)

## Qué es esto
Prototipo interactivo (clicable, no solo mockup) de la plataforma descrita en el brief: bolsa de trabajo segmentada por comunidad académica de la Facultad de Ingeniería, USAC. Construido sobre el sistema de diseño Industry (wireframe azulado, tipografía Barlow/Barlow Condensed, tarjetas con marcas de esquina), ahora en modo oscuro con acento lavanda/azul.

## Roles cubiertos
- **Buscador de empleo (estudiante/egresado)** — completo
- **Empresa/institución** — completo
- **Empleado saliente (referidor)** — completo
- **Moderador** — completo

## Qué hemos logrado, por sprint del brief

**Sprint 1 — Fundamentos visuales y estructura**
- Identidad visual sobre Industry: paleta (ahora lavanda/azul), tipografía, iconografía Lucide, fondo tipo cuadrícula técnica sutil.
- Navegación por rol: pantalla de inicio con las 4 tarjetas de rol como mapa de navegación funcional.

**Sprint 2 — Onboarding y perfiles**
- Registro del buscador de empleo: cuenta (correo institucional, contraseña, teléfono), datos personales, datos académicos (carrera, semestre, créditos, estado activo/EPS/graduado), portafolio (bio, CV).
- Registro de empresa (nombre, correo de contacto, sector, sitio web).
- Registro de referidor (nombre, correo, carrera de la que egresó).
- Perfil público del buscador (info de contacto + académica, barra de progreso de créditos).

**Sprint 3 — Publicación y descubrimiento**
- Formulario de publicación de vacante (empresa): puesto, carrera compatible, semestre mínimo, modalidad, contrato, ubicación, descripción, requisitos.
- Formulario de publicación de referido: puesto, empresa, carrera, semestre mínimo, modalidad, contrato, nota personal, enlace oficial opcional.
- Feed de vacantes con filtros (carrera, semestre mínimo, tipo de contrato) y contador de resultados.
- Tarjeta diferenciada: empresa (marco blueprint, tag sólido) vs. referido (borde punteado, tono lavanda, cita personal).
- Vista de detalle de vacante para ambos tipos.

**Sprint 4 — Postulación y panel de moderación**
- Postulación de un clic desde el detalle de la vacante.
- Estados de postulación (enviada, en revisión, aceptada, rechazada) en "Mis postulaciones".
- Panel de moderación: cola de verificación + historial, diálogo de revisión con aprobar/rechazar.
- **Ciclo cerrado:** una vacante o recomendación publicada entra a la cola de moderación; al aprobarse, aparece automáticamente en el feed de estudiantes.

**Sprint 5 — parcial**
- Notificaciones (vacante compatible, cambio de estado de postulación).
- Estado vacío en "Mis postulaciones" y en el feed sin resultados.
- Pendiente: bocetos de reputación y de "vacantes externas" (scraping), y más estados de error/carga.

## Decisiones de estilo recientes
- Modo oscuro: fondo oscuro, paneles (navs, formularios, feed, cola de moderación) con su propio fondo para legibilidad, botones con relleno propio distinto del panel.
- Paleta recoloreada a un duotono frío: azul (acento principal — CTAs, empresa) y lavanda/morado (acento secundario — referidos, estados "pendiente"), definidos en OKLCH sobre las mismas rampas del sistema.

## Supuestos marcados (pendientes de validar con datos reales)
- Listado de escuelas/carreras de la Facultad de Ingeniería (simplificado a 6 carreras).
- Verificación institucional real vía correo @usac.edu.gt — no implementada (fuera de alcance de diseño).
- Datos de empresas, vacantes y cola de moderación son de ejemplo.

## Qué falta / fuera de alcance actual
- Registro de empresa/referidor con verificación real (@usac.edu.gt, documentación fiscal).
- Boceto de sistema de reputación/valoración (Sprint 5).
- Boceto de "vacantes externas relevantes" vía scraping (Sprint 5).
- Estados de error y de carga más allá de los vacíos ya cubiertos.
- Backend, autenticación real y el bot de scraping — explícitamente fuera de alcance de diseño (brief, sección 7).

## Cómo navegar el prototipo
- Entra como "Buscador de empleo" para el flujo de estudiante, o usa las tarjetas de "Empresa" / "Empleado saliente" desde la misma pantalla de inicio.
- El enlace "¿Eres moderador?" en esa misma pantalla lleva al panel de moderación.
- Los tweaks del componente (`initialMode`, `demoDataPrefill`, `showAssumptionNotes`) permiten arrancar directo en un rol o mostrar/ocultar las notas de supuestos.
