from pydantic import BaseModel, Field, ConfigDict, AliasChoices
from typing import Optional, Any, List
from datetime import datetime, date, time

# Clase base única para todos los esquemas para evitar problemas de MRO
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# --- ASISTENCIA ---
class AsistenciaBase(BaseSchema):
    id: Any
    entrenamiento: Optional[Any] = Field(None, validation_alias=AliasChoices("entrenamiento", "entrenamiento_id"), serialization_alias="entrenamiento")
    jugador: Optional[Any] = Field(None, validation_alias=AliasChoices("jugador", "jugador_id"), serialization_alias="jugador")
    asistencia: Optional[str] = None

class AsistenciaCreate(BaseModel): # Create schemas don't need from_attributes
    entrenamiento_id: Any
    jugador_id: Any
    asistencia: str

class AsistenciaResponse(AsistenciaBase):
    entrenamientos: Optional['EntrenamientosConEventoResponse'] = None
    jugadores: Optional['JugadoresPropiosResponse'] = None

# --- ESTADISTICAS PARTIDO ---
class EstadisticasPartidoBase(BaseSchema):
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

    # Advanced Metrics
    posesion_local: Optional[int] = None
    posesion_visitante: Optional[int] = None
    placajes_hechos_local: Optional[int] = None
    placajes_hechos_visitante: Optional[int] = None
    placajes_fallados_local: Optional[int] = None
    placajes_fallados_visitante: Optional[int] = None
    mele_ganada_local: Optional[int] = None
    mele_ganada_visitante: Optional[int] = None
    mele_perdida_local: Optional[int] = None
    mele_perdida_visitante: Optional[int] = None
    touch_ganada_local: Optional[int] = None
    touch_ganada_visitante: Optional[int] = None
    touch_perdida_local: Optional[int] = None
    touch_perdida_visitante: Optional[int] = None

class EstadisticasPartidoResponse(EstadisticasPartidoBase):
    pass

class EstadisticasPartidoCreate(BaseModel):
    id: Optional[str] = None
    fecha: Optional[date] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    ensayos_local: Optional[int] = None
    ensayos_visitante: Optional[int] = None
    partido_id: Optional[str] = None
    partido_externo_id: Optional[str] = None
    jornada: Optional[int] = None
    acta_procesada: Optional[bool] = None
    posesion_local: Optional[int] = None
    posesion_visitante: Optional[int] = None
    placajes_hechos_local: Optional[int] = None
    placajes_hechos_visitante: Optional[int] = None
    placajes_fallados_local: Optional[int] = None
    placajes_fallados_visitante: Optional[int] = None
    mele_ganada_local: Optional[int] = None
    mele_ganada_visitante: Optional[int] = None
    mele_perdida_local: Optional[int] = None
    mele_perdida_visitante: Optional[int] = None
    touch_ganada_local: Optional[int] = None
    touch_ganada_visitante: Optional[int] = None
    touch_perdida_local: Optional[int] = None
    touch_perdida_visitante: Optional[int] = None

class EstadisticasPartidoUpdate(BaseModel):
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    ensayos_local: Optional[int] = None
    ensayos_visitante: Optional[int] = None
    jornada: Optional[int] = None
    acta_procesada: Optional[bool] = None
    fecha: Optional[date] = None
    posesion_local: Optional[int] = None
    posesion_visitante: Optional[int] = None
    placajes_hechos_local: Optional[int] = None
    placajes_hechos_visitante: Optional[int] = None
    placajes_fallados_local: Optional[int] = None
    placajes_fallados_visitante: Optional[int] = None
    mele_ganada_local: Optional[int] = None
    mele_ganada_visitante: Optional[int] = None
    mele_perdida_local: Optional[int] = None
    mele_perdida_visitante: Optional[int] = None
    touch_ganada_local: Optional[int] = None
    touch_ganada_visitante: Optional[int] = None
    touch_perdida_local: Optional[int] = None
    touch_perdida_visitante: Optional[int] = None

# --- ENTRENAMIENTOS ---
class EntrenamientosBase(BaseSchema):
    id_entrenamiento: Any
    evento: Optional[Any] = None
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None
    trabajo_separado: Optional[str] = None
    trabajo_conjunto: Optional[str] = None
    calentamiento: Optional[str] = None

class EntrenamientosResponse(EntrenamientosBase):
    pass

class EntrenamientosDetalleResponse(EntrenamientosBase):
    evento_ref: Optional['EventosResponse'] = None
    asistencias: Optional[List['AsistenciaResponse']] = []

class EntrenamientosConEventoResponse(EntrenamientosBase):
    evento_ref: Optional['EventosResponse'] = None

# --- RIVALES ---
class RivalesBase(BaseSchema):
    id_equipo: Any
    nombre_equipo: Optional[str] = None
    escudo: Optional[str] = None
    ciudad: Optional[str] = None
    categoria: Optional[str] = None
    temporada: Optional[str] = None
    fecha_creacion: Optional[datetime] = None

class RivalesResponse(RivalesBase):
    pass

# --- EVENTOS ---
class EventosBase(BaseSchema):
    id: Any
    fecha: Optional[date] = None
    hora: Optional[time] = None
    tipo: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None
    created_at: Optional[datetime] = None

class EventosResponse(EventosBase):
    partido: Optional['PartidosResponse'] = None
    entrenamiento: Optional['EntrenamientosResponse'] = None
    analisis: Optional['AnalisisPartidoResponse'] = None

class EventoCreateUpdate(BaseModel):
    id: Optional[str] = None # UUID if updating
    tipo: str
    fecha: date
    hora: time
    estado: Optional[str] = "Programado"
    observaciones: Optional[str] = None
    
    # Training details (optional, used if tipo == 'Entrenamiento')
    calentamiento: Optional[str] = None
    trabajo_separado: Optional[str] = None
    trabajo_conjunto: Optional[str] = None
    
    # Match details (optional, used if tipo == 'Partido')
    rival_id: Optional[str] = None
    es_local: Optional[bool] = True
    lugar: Optional[str] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    jornada: Optional[int] = None

EventosResponse.model_rebuild()
AsistenciaResponse.model_rebuild()
PartidosResponse.model_rebuild()
PartidosExternosResponse.model_rebuild()
EntrenamientosDetalleResponse.model_rebuild()
EntrenamientosConEventoResponse.model_rebuild()
