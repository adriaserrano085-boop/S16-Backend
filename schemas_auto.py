from pydantic import BaseModel, Field, ConfigDict, AliasChoices
from typing import Optional, Any, List
from datetime import datetime, date, time

# Configuración base para todos los esquemas de respuesta
# Importante: BaseResponse YA HEREDA de BaseModel.
class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# --- ASISTENCIA ---
class AsistenciaBase(BaseModel):
    id: Any
    entrenamiento: Optional[Any] = Field(None, validation_alias=AliasChoices("entrenamiento", "entrenamiento_id"), serialization_alias="entrenamiento")
    jugador: Optional[Any] = Field(None, validation_alias=AliasChoices("jugador", "jugador_id"), serialization_alias="jugador")
    asistencia: Optional[str] = None

class AsistenciaCreate(BaseModel):
    entrenamiento_id: Any
    jugador_id: Any
    asistencia: str

class AsistenciaResponse(AsistenciaBase, BaseResponse):
    pass

# --- ESTADISTICAS PARTIDO ---
class EstadisticasPartidoBase(BaseModel):
    id: Any
    fecha: Optional[date] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    ensayos_local: Optional[int] = None
    ensayos_visitante: Optional[int] = None
    partido: Optional[Any] = Field(None, validation_alias=AliasChoices("partido", "partido_id"), serialization_alias="partido")
    partido_externo: Optional[Any] = Field(None, validation_alias=AliasChoices("partido_externo", "partido_externo_id"), serialization_alias="partido_externo")
    jornada: Optional[int] = None
    acta_procesada: Optional[bool] = None
    fecha_procesado: Optional[datetime] = None

class EstadisticasPartidoResponse(EstadisticasPartidoBase, BaseResponse):
    pass

# --- ENTRENAMIENTOS ---
class EntrenamientosBase(BaseModel):
    id_entrenamiento: Any
    evento: Optional[Any] = None
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None
    trabajo_separado: Optional[str] = None
    trabajo_conjunto: Optional[str] = None
    calentamiento: Optional[str] = None

class EntrenamientosResponse(EntrenamientosBase, BaseResponse):
    pass

# --- RIVALES ---
class RivalesBase(BaseModel):
    id_equipo: Any
    nombre_equipo: Optional[str] = None
    escudo: Optional[str] = None
    ciudad: Optional[str] = None
    categoria: Optional[str] = None
    temporada: Optional[str] = None
    fecha_creacion: Optional[datetime] = None

class RivalesResponse(RivalesBase, BaseResponse):
    pass

# --- EVENTOS ---
class EventosBase(BaseModel):
    id: Any
    fecha: Optional[date] = None
    hora: Optional[time] = None
    tipo: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None
    created_at: Optional[datetime] = None

class EventosResponse(EventosBase, BaseResponse):
    pass

# --- PARTIDOS ---
class PartidosBase(BaseModel):
    id: Any
    Rival: Optional[Any] = None
    Evento: Optional[Any] = None
    es_local: Optional[bool] = None
    marcador_local: Optional[float] = None
    marcador_visitante: Optional[float] = None
    ensayos_local: Optional[int] = None
    ensayos_visitante: Optional[int] = None
    jornada: Optional[int] = None
    lugar: Optional[str] = None
    observaciones: Optional[str] = None
    acta_url: Optional[str] = None

class PartidosResponse(PartidosBase, BaseResponse):
    pass

# --- PARTIDOS EXTERNOS ---
class PartidosExternosBase(BaseModel):
    id: Any
    equipo_local: Optional[str] = None
    equipo_visitante: Optional[str] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    ensayos_local: Optional[int] = None
    ensayos_visitante: Optional[int] = None
    fecha: Optional[date] = None
    jornada: Optional[int] = None
    competicion: Optional[str] = None

class PartidosExternosResponse(PartidosExternosBase, BaseResponse):
    pass

# --- ESTADISTICAS JUGADOR ---
class EstadisticasJugadorBase(BaseModel):
    id: Any
    partido: Optional[Any] = None
    jugador: Optional[Any] = None
    partido_externo: Optional[Any] = None
    jugador_externo: Optional[Any] = None
    nombre: Optional[str] = None
    equipo: Optional[str] = None
    dorsal: Optional[int] = None
    ensayos: Optional[int] = 0
    transformaciones: Optional[int] = 0
    penales: Optional[int] = 0
    drops: Optional[int] = 0
    tarjetas_amarillas: Optional[int] = 0
    tarjetas_rojas: Optional[int] = 0
    minutos_jugados: Optional[int] = None
    es_titular: Optional[bool] = None
    es_capitan: Optional[bool] = None

class EstadisticasJugadorResponse(EstadisticasJugadorBase, BaseResponse):
    pass

# --- ANALISIS PARTIDO ---
class AnalisisPartidoBase(BaseModel):
    id: Any
    partido: Optional[Any] = Field(None, validation_alias=AliasChoices("partido", "partido_id"), serialization_alias="partido")
    evento: Optional[Any] = Field(None, validation_alias=AliasChoices("evento", "evento_id"), serialization_alias="evento")
    partido_externo: Optional[Any] = Field(None, validation_alias=AliasChoices("partido_externo", "partido_externo_id"), serialization_alias="partido_externo")
    video_url: Optional[str] = None
    video_offset_sec: Optional[int] = None
    raw_json: Optional[str] = None

class AnalisisPartidoResponse(AnalisisPartidoBase, BaseResponse):
    pass

# --- OTROS ---
class StaffResponse(BaseResponse): # Corregido: eliminado BaseModel redundante
    id: Any
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None
    activo: Optional[bool] = None

class JugadoresPropiosResponse(BaseResponse): # Corregido: eliminado BaseModel redundante
    id: Any
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None
    posiciones: Optional[str] = None
    activo: Optional[bool] = None

class FamiliasResponse(BaseResponse): # Corregido: eliminado BaseModel redundante
    id_usuario: Any
    nombre_completo: Optional[str] = None
    parentesco: Optional[str] = None

class ConvocatoriaResponse(BaseResponse): # Corregido: eliminado BaseModel redundante
    id: Any
    partido: Optional[Any] = None
    jugador: Optional[Any] = None
    numero: Optional[float] = None
