from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime, date, time

# Usamos los nombres EXACTOS de la base de datos para evitar problemas de mapeo
# y configuramos Pydantic para que permita alias si el frontend los necesita.

class AsistenciaBase(BaseModel):
    id: Any
    entrenamiento_id: Optional[Any] = Field(None, alias="entrenamiento")
    jugador_id: Optional[Any] = Field(None, alias="jugador")
    asistencia: Optional[str] = None

class AsistenciaCreate(BaseModel):
    entrenamiento_id: Any
    jugador_id: Any
    asistencia: str

class AsistenciaResponse(AsistenciaBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

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

class EstadisticasPartidoResponse(EstadisticasPartidoBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class EntrenamientosBase(BaseModel):
    id_entrenamiento: Any
    evento: Optional[Any] = None
    fecha: Optional[date] = None # Aunque no esté en el modelo ORM, lo añadimos si el frontend lo busca
    trabajo_separado: Optional[str] = None
    trabajo_conjunto: Optional[str] = None
    calentamiento: Optional[str] = None

class EntrenamientosResponse(EntrenamientosBase):
    model_config = ConfigDict(from_attributes=True)

class RivalesBase(BaseModel):
    id_equipo: Any
    nombre_equipo: Optional[str] = None
    escudo: Optional[str] = None
    ciudad: Optional[str] = None
    categoria: Optional[str] = None
    temporada: Optional[str] = None

class RivalesResponse(RivalesBase):
    model_config = ConfigDict(from_attributes=True)

class EventosBase(BaseModel):
    id: Any
    fecha: Optional[date] = None
    hora: Optional[time] = None
    tipo: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None

class EventosResponse(EventosBase):
    model_config = ConfigDict(from_attributes=True)

class PartidosBase(BaseModel):
    id: Any
    Rival: Optional[Any] = None
    Evento: Optional[Any] = None
    es_local: Optional[bool] = None
    marcador_local: Optional[float] = None
    marcador_visitante: Optional[float] = None

class PartidosResponse(PartidosBase):
    model_config = ConfigDict(from_attributes=True)

class PartidosExternosBase(BaseModel):
    id: Any
    equipo_local: Optional[str] = None
    equipo_visitante: Optional[str] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    fecha: Optional[date] = None

class PartidosExternosResponse(PartidosExternosBase):
    model_config = ConfigDict(from_attributes=True)

class EstadisticasJugadorBase(BaseModel):
    id: Any
    partido: Optional[Any] = None
    jugador: Optional[Any] = None
    nombre: Optional[str] = None
    equipo: Optional[str] = None
    ensayos: Optional[int] = 0
    tarjetas_amarillas: Optional[int] = 0
    tarjetas_rojas: Optional[int] = 0

class EstadisticasJugadorResponse(EstadisticasJugadorBase):
    model_config = ConfigDict(from_attributes=True)

# Esquemas para los otros modelos (mantenemos nombres originales por ahora)
class StaffResponse(BaseModel):
    id: Any
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class JugadoresPropiosResponse(BaseModel):
    id: Any
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class FamiliasResponse(BaseModel):
    id_usuario: Any
    nombre_completo: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
