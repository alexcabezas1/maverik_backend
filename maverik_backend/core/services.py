import logging

import requests
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Query, Session

from maverik_backend.core import schemas
from maverik_backend.core.models import SesionAsesoria, SesionAsesoriaDetalle, Usuario


def crear_usuario(db: Session, valores: schemas.UsuarioCrear) -> Usuario:
    usuario = Usuario(
        email=valores.email,
        clave=valores.clave,
        fecha_nacimiento=valores.fecha_nacimiento,
        nivel_educativo_id=valores.nivel_educativo_id,
        conocimiento_alt_inversion_id=valores.conocimiento_alt_inversion_id,
        experiencia_invirtiendo_id=valores.experiencia_invirtiendo_id,
        porcentaje_ahorro_mensual_id=valores.porcentaje_ahorro_mensual_id,
        porcentaje_ahorro_invertir_id=valores.porcentaje_ahorro_invertir_id,
        tiempo_mantener_inversion_id=valores.tiempo_mantener_inversion_id,
        busca_invertir_en_id=valores.busca_invertir_en_id,
        proporcion_inversion_mantener_id=valores.proporcion_inversion_mantener_id,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


def crear_sesion_asesoria(db: Session, valores: schemas.SesionAsesoriaCrear) -> SesionAsesoria:
    sesion_asesoria = SesionAsesoria(
        objetivo_id=valores.objetivo_id,
        usuario_id=valores.usuario_id,
        capital_inicial=valores.capital_inicial,
        horizonte_temporal_anios=valores.horizonte_temporal_anios,
        tolerancia_al_riesgo_id=valores.tolerancia_al_riesgo_id,
    )
    db.add(sesion_asesoria)
    db.commit()
    db.refresh(sesion_asesoria)

    return sesion_asesoria


def crear_sesion_asesoria_detalle(
    db: Session,
    valores: schemas.SesionAsesoriaDetalleCrear,
) -> SesionAsesoriaDetalle:
    detalle = SesionAsesoriaDetalle(
        sesion_asesoria_id=valores.sesion_asesoria_id,
        texto_usuario=valores.texto_usuario,
        texto_sistema=valores.texto_sistema,
    )
    db.add(detalle)
    db.commit()
    db.refresh(detalle)

    return detalle


def verificar_usuario(db: Session, data: schemas.UsuarioLogin) -> Usuario | None:
    query = Query(Usuario).filter(
        Usuario.email == data.email,
        Usuario.clave == data.clave,
    )
    try:
        return query.with_session(db).one()
    except NoResultFound:
        return None


def cargar_sesion_asesoria_detalles(db: Session, sesion_asesoria_id: int) -> list[SesionAsesoriaDetalle]:
    query = Query(SesionAsesoriaDetalle).filter_by(sesion_asesoria_id=sesion_asesoria_id)
    try:
        return query.with_session(db).all()
    except NoResultFound:
        return None


def mantener_servicios_activos(urls: list[str]):
    for url in urls:
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                logging.info("Llamada exitosa al servicio {}".format(url))
            else:
                logging.info("Error en la llamada al servicio: Código {}".format(respuesta.status_code))
        except Exception as e:
            print("Ocurrió un error: {}".format(e))
