from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class UsuarioCrear(BaseModel):
    email: EmailStr
    clave: str
    fecha_nacimiento: date
    nivel_educativo_id: int
    conocimiento_alt_inversion_id: int
    experiencia_invirtiendo_id: int
    porcentaje_ahorro_mensual_id: int
    porcentaje_ahorro_invertir_id: int
    tiempo_mantener_inversion_id: int
    busca_invertir_en_id: int
    proporcion_inversion_mantener_id: int


class UsuarioActualizar(BaseModel):
    fecha_actualizacion: datetime


class Usuario(BaseModel):
    id: int
    email: EmailStr
    fecha_nacimiento: date
    nivel_educativo_id: int
    conocimiento_alt_inversion_id: int
    experiencia_invirtiendo_id: int
    porcentaje_ahorro_mensual_id: int
    porcentaje_ahorro_invertir_id: int
    tiempo_mantener_inversion_id: int
    busca_invertir_en_id: int
    proporcion_inversion_mantener_id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    email: EmailStr
    clave: str


class SesionAsesoriaCrear(BaseModel):
    objetivo_id: int
    usuario_id: int
    capital_inicial: float
    horizonte_temporal_anios: int
    tolerancia_al_riesgo_id: int


class SesionAsesoria(BaseModel):
    id: int
    objetivo_id: int
    usuario_id: int
    capital_inicial: float
    horizonte_temporal_anios: int
    tolerancia_al_riesgo_id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class SesionAsesoriaDetalleCrear(BaseModel):
    sesion_asesoria_id: int
    texto_usuario: str
    texto_sistema: str


class SesionAsesoriaDetalle(BaseModel):
    id: int
    sesion_asesoria_id: int
    texto_usuario: str
    texto_sistema: str


class SesionAsesoriaConDetalles(BaseModel):
    id: int
    detalles: list[SesionAsesoriaDetalle]


class UsuarioCrearRequest(BaseModel):
    email: str
    clave: str
    fecha_nacimiento: date
    nivel_educativo_id: int
    conocimiento_alt_inversion_id: int
    experiencia_invirtiendo_id: int
    porcentaje_ahorro_mensual_id: int
    porcentaje_ahorro_invertir_id: int
    tiempo_mantener_inversion_id: int
    busca_invertir_en_id: int
    proporcion_inversion_mantener_id: int


class SesionAsesoriaCrearRequest(BaseModel):
    objetivo_id: int
    capital_inicial: float
    horizonte_temporal_anios: int
    tolerancia_al_riesgo_id: int


class SesionAsesoriaDetalleRequest(BaseModel):
    texto_usuario: str
    texto_sistema: str
