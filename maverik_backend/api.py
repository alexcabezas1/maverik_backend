import logging
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from maverik_backend.core import schemas, services
from maverik_backend.core.database import get_sessionmaker
from maverik_backend.settings import Settings, load_config
from maverik_backend.utils import auth

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

app_config: Settings = load_config()

app = FastAPI()
secret_key = b"k4.local.doPhJGTf4E4lAtRrC8WKUmr18LwF6T_r-kI9D1C_J-k="  # TODO: auth.create_symmetric_key()


# Dependency
def obtener_db():
    SessionLocal = get_sessionmaker(app_config)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def raiz():
    return {"service": "maverik_backend"}


@app.post("/user/signup", response_model=schemas.Usuario, tags=["user"])
async def crear_usuario(
    data: schemas.UsuarioCrearRequest,
    db: Annotated[Session, Depends(obtener_db)],
):
    clave = secrets.token_urlsafe(20)
    valores = schemas.UsuarioCrear(
        email=data.email,
        clave=clave,
        fecha_nacimiento=data.fecha_nacimiento,
        nivel_educativo_id=data.nivel_educativo_id,
        conocimiento_alt_inversion_id=data.conocimiento_alt_inversion_id,
        experiencia_invirtiendo_id=data.experiencia_invirtiendo_id,
        porcentaje_ahorro_mensual_id=data.porcentaje_ahorro_mensual_id,
        porcentaje_ahorro_invertir_id=data.porcentaje_ahorro_invertir_id,
        tiempo_mantener_inversion_id=data.tiempo_mantener_inversion_id,
        busca_invertir_en_id=data.busca_invertir_en_id,
        proporcion_inversion_mantener_id=data.proporcion_inversion_mantener_id,
    )

    usuario = services.crear_usuario(db=db, valores=valores)

    # enviar correo

    return usuario


@app.post("/user/login", tags=["user"])
async def login_usuario(
    data: schemas.UsuarioLogin,
    db: Annotated[Session, Depends(obtener_db)],
):
    usuario = services.verificar_usuario(db, data)
    if usuario:
        return auth.sign(str(usuario.id), key=secret_key)
    else:
        return {"error": "Wrong login details!"}


@app.post("/copilot/sessions", response_model=schemas.SesionAsesoria, tags=["copilot"])
async def nueva_sesion_asesoria(
    data: schemas.SesionAsesoriaCrearRequest,
    auth_token: Annotated[bytes, Depends(auth.PasetoBearer(key=secret_key))],
    db: Annotated[Session, Depends(obtener_db)],
):
    sesion_asesoria = None
    auth_payload = auth.decode(token=auth_token, key=secret_key)
    if auth_payload:
        usuario_id = auth_payload["user_id"]

        valores = schemas.SesionAsesoriaCrear(
            objetivo_id=data.objetivo_id,
            usuario_id=usuario_id,
            capital_inicial=data.capital_inicial,
            horizonte_temporal_anios=data.horizonte_temporal_anios,
            tolerancia_al_riesgo_id=data.tolerancia_al_riesgo_id,
        )

        sesion_asesoria = services.crear_sesion_asesoria(db=db, valores=valores)

    return sesion_asesoria
