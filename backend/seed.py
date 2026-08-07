"""
Script de seed para poblar la BD con datos de prueba.
Ejecutar desde backend/: python seed.py
"""
from app.database import SessionLocal, engine, Base
import app.models.usuario      # noqa: F401
import app.models.vacante      # noqa: F401
import app.models.postulacion  # noqa: F401
import app.models.certificacion  # noqa: F401
import app.models.notificacion  # noqa: F401

from app.models.usuario import Usuario, TipoUsuario, EstadoAcademico, NivelVerificacion
from app.models.vacante import Vacante, TipoVacante, Modalidad, TipoContrato, EstadoVacante
from app.models.postulacion import Postulacion
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()


def seed():
    if db.query(Usuario).count() > 0:
        print("La BD ya tiene datos. Limpia usac_empleos.db para re-sembrar.")
        return

    # Usuarios de prueba
    estudiante = Usuario(
        email="estudiante@usac.edu.gt",
        password_hash=get_password_hash("password123"),
        tipo_usuario=TipoUsuario.estudiante,
        nombre="Ana García",
        telefono="5550-1234",
        carrera="Ingeniería en Ciencias y Sistemas",
        escuela="ECYS",
        semestre=7,
        creditos_aprobados=180,
        estado_academico=EstadoAcademico.activo,
        bio="Desarrolladora apasionada por el backend y los sistemas distribuidos.",
        github_url="https://github.com/anagarcia",
        nivel_verificacion=NivelVerificacion.basico,
    )

    empresa = Usuario(
        email="empresa@techgt.com",
        password_hash=get_password_hash("password123"),
        tipo_usuario=TipoUsuario.empresa,
        nombre="Carlos Méndez",
        nombre_empresa="TechGT S.A.",
        sector="Tecnología",
        sitio_web="https://techgt.com",
    )

    referidor = Usuario(
        email="referidor@gmail.com",
        password_hash=get_password_hash("password123"),
        tipo_usuario=TipoUsuario.referidor,
        nombre="Luis Pérez",
        carrera_egresada="Ingeniería en Ciencias y Sistemas",
    )

    moderador = Usuario(
        email="moderador@usac.edu.gt",
        password_hash=get_password_hash("password123"),
        tipo_usuario=TipoUsuario.moderador,
        nombre="Moderador FIUSAC",
    )

    db.add_all([estudiante, empresa, referidor, moderador])
    db.commit()
    db.refresh(empresa)
    db.refresh(referidor)
    db.refresh(estudiante)

    # Vacante de empresa (pendiente — espera moderación)
    vacante_pendiente = Vacante(
        tipo=TipoVacante.empresa,
        publicador_id=empresa.id,
        puesto="Desarrollador Backend Junior",
        empresa_nombre="TechGT S.A.",
        carrera_compatible="Ingeniería en Ciencias y Sistemas",
        semestre_minimo=6,
        modalidad=Modalidad.hibrido,
        tipo_contrato=TipoContrato.tiempo_completo,
        ubicacion="Guatemala City",
        descripcion="Buscamos un desarrollador backend con conocimientos en Python o Java.",
        requisitos="Python o Java, SQL básico, Git.",
        solo_plataforma=True,
        estado=EstadoVacante.pendiente,
    )

    # Vacante aprobada (ya visible en el feed)
    vacante_aprobada = Vacante(
        tipo=TipoVacante.empresa,
        publicador_id=empresa.id,
        puesto="Analista de Datos",
        empresa_nombre="TechGT S.A.",
        carrera_compatible="Ingeniería en Ciencias y Sistemas",
        semestre_minimo=5,
        modalidad=Modalidad.remoto,
        tipo_contrato=TipoContrato.medio_tiempo,
        ubicacion="Remoto",
        descripcion="Análisis de datos con Python y SQL. Horario flexible.",
        requisitos="Python, SQL, estadística básica.",
        estado=EstadoVacante.aprobada,
    )

    # Vacante de referido
    vacante_referida = Vacante(
        tipo=TipoVacante.referido,
        publicador_id=referidor.id,
        puesto="Junior DevOps Engineer",
        empresa_nombre="Startup XYZ",
        carrera_compatible="Ingeniería en Ciencias y Sistemas",
        semestre_minimo=8,
        modalidad=Modalidad.presencial,
        tipo_contrato=TipoContrato.tiempo_completo,
        ubicacion="Zona 10, Guatemala",
        descripcion="Posición que dejo disponible al cambiarme de empresa.",
        nota_personal="Es un equipo muy bueno, aprenderás mucho de infraestructura cloud.",
        enlace_oficial="https://startup-xyz.com/jobs/devops",
        estado=EstadoVacante.aprobada,
    )

    db.add_all([vacante_pendiente, vacante_aprobada, vacante_referida])
    db.commit()

    print("✓ Seed completado. Usuarios de prueba:")
    print("  estudiante@usac.edu.gt  / password123  (estudiante)")
    print("  empresa@techgt.com      / password123  (empresa)")
    print("  referidor@gmail.com     / password123  (referidor)")
    print("  moderador@usac.edu.gt   / password123  (moderador)")
    print("\n  Docs API: http://localhost:8000/api/docs")

    db.close()


if __name__ == "__main__":
    seed()
