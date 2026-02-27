from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, List
from datetime import datetime, date, time

# Configuración base para todos los esquemas de respuesta
class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class AsistenciaBase(BaseModel):
    id: Any
    entrenamiento_id: Optional[Any] = Field(None, alias="entrenamiento")
    jugador_id: Optional[Any] = Field(None, alias="jugador")
    asistencia: Optional[str] = None

class AsistenciaCreate(BaseModel):
    entrenamiento_id: Any
    jugador_id: Any
    asistencia: str

class AsistenciaResponse(AsistenciaBase, BaseResponse):
    pass

class EstadisticasPartidoBase(BaseModel):
    id: Any
    fecha: Optional[date] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    ensayos_local: Optional[int] = None
    ensayos_visitante: Optional[int] = None
    partido_id: Optional[Any] = Field(None, alias="partido")
    partido_externo_id: Optional[Any] = Field(None, alias="partido_externo")
    jornada: Optional[int] = None

class EstadisticasPartidoResponse(EstadisticasPartidoBase, BaseResponse):
    pass

class EntrenamientosBase(BaseModel):
    id_entrenamiento: Any
    evento: Optional[Any] = None
    fecha: Optional[date] = None
    trabajo_separado: Optional[str] = None
    trabajo_conjunto: Optional[str] = None
    calentamiento: Optional[str] = None

class EntrenamientosResponse(EntrenamientosBase, BaseResponse):
    pass

class RivalesBase(BaseModel):
    id_equipo: Any
    nombre_equipo: Optional[str] = None
    escudo: Optional[str] = None
    ciudad: Optional[str] = None
    categoria: Optional[str] = None
    temporada: Optional[str] = None

class RivalesResponse(RivalesBase, BaseResponse):
    pass

class EventosBase(BaseModel):
    id: Any
    fecha: Optional[date] = None
    hora: Optional[time] = None
    tipo: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None

class EventosResponse(EventosBase, BaseResponse):
    pass

class PartidosBase(BaseModel):
    id: Any
    Rival: Optional[Any] = None
    Evento: Optional[Any] = None
    es_local: Optional[bool] = None
    marcador_local: Optional[float] = None
    marcador_visitante: Optional[float] = None

class PartidosResponse(PartidosBase, BaseResponse):
    pass

class PartidosExternosBase(BaseModel):
    id: Any
    equipo_local: Optional[str] = None
    equipo_visitante: Optional[str] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    fecha: Optional[date] = None

class PartidosExternosResponse(PartidosExternosBase, BaseResponse):
    pass

class EstadisticasJugadorBase(BaseModel):
    id: Any
    partido: Optional[Any] = None
    jugador: Optional[Any] = None
    nombre: Optional[str] = None
    equipo: Optional[str] = None
    ensayos: Optional[int] = 0
    tarjetas_amarillas: Optional[int] = 0
    tarjetas_rojas: Optional[int] = 0

class EstadisticasJugadorResponse(EstadisticasJugadorBase, BaseResponse):
    pass

class AnalisisPartidoBase(BaseModel):
    id: Any
    partido_id: Optional[Any] = Field(None, alias="partido")
    evento_id: Optional[Any] = Field(None, alias="evento")
    partido_externo_id: Optional[Any] = Field(None, alias="partido_externo")
    video_url: Optional[str] = None
    video_offset_sec: Optional[int] = None
    raw_json: Optional[str] = None

class AnalisisPartidoResponse(AnalisisPartidoBase, BaseResponse):
    pass

class StaffResponse(BaseModel, BaseResponse):
    id: Any
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None

class JugadoresPropiosResponse(BaseModel, BaseResponse):
    id: Any
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None

class FamiliasResponse(BaseModel, BaseResponse):
    id_usuario: Any
    nombre_completo: Optional[str] = None

class ConvocatoriaResponse(BaseModel, BaseResponse):
    id: Any
    partido: Optional[Any] = None
    jugador: Optional[Any] = None
    numero: Optional[float] = None
