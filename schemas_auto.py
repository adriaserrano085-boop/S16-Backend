from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime, date, time

class AsistenciaBase(BaseModel):
    id: Any
    entrenamiento: Optional[Any] = Field(None, validation_alias="entrenamiento_id")
    jugador: Optional[Any] = Field(None, validation_alias="jugador_id")
    asistencia: Optional[str] = None

class AsistenciaCreate(BaseModel):
    entrenamiento_id: Optional[Any] = None
    jugador_id: Optional[Any] = None
    asistencia: Optional[str] = None

class AsistenciaUpdate(BaseModel):
    asistencia: Optional[str] = None

class AsistenciaResponse(AsistenciaBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class EstadisticasPartidoBase(BaseModel):
    fecha: Optional[date] = None
    ensayos_local: Optional[int] = None
    ensayos_visitante: Optional[int] = None
    jornada: Optional[int] = None
    acta_procesada: Optional[bool] = None
    fecha_procesado: Optional[datetime] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    partido: Optional[Any] = Field(None, validation_alias="partido_id")
    partido_externo: Optional[Any] = Field(None, validation_alias="partido_externo_id")
    id: Any

class EstadisticasPartidoCreate(BaseModel):
    fecha: Optional[date] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    partido_id: Optional[Any] = None
    partido_externo_id: Optional[Any] = None

class EstadisticasPartidoResponse(EstadisticasPartidoBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class EntrenamientosBase(BaseModel):
    trabajo_separado: Optional[str] = None
    id_entrenamiento: Any
    evento: Optional[Any] = None
    trabajo_conjunto: Optional[str] = None
    calentamiento: Optional[str] = None

class EntrenamientosCreate(BaseModel):
    id_entrenamiento: Any
    evento: Optional[Any] = None

class EntrenamientosResponse(EntrenamientosBase):
    model_config = ConfigDict(from_attributes=True)

class RivalesBase(BaseModel):
    id_equipo: Any
    ciudad: Optional[str] = None
    escudo: Optional[str] = None
    categoria: Optional[str] = None
    temporada: Optional[str] = None
    nombre_equipo: Optional[str] = None

class RivalesCreate(RivalesBase):
    pass

class RivalesResponse(RivalesBase):
    model_config = ConfigDict(from_attributes=True)

class StaffBase(BaseModel):
    id: Any
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None

class StaffCreate(StaffBase):
    pass

class StaffResponse(StaffBase):
    model_config = ConfigDict(from_attributes=True)

class JugadoresPropiosBase(BaseModel):
    id: Any
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None
    posiciones: Optional[str] = None

class JugadoresPropiosCreate(JugadoresPropiosBase):
    pass

class JugadoresPropiosResponse(JugadoresPropiosBase):
    model_config = ConfigDict(from_attributes=True)

class FamiliasBase(BaseModel):
    id_usuario: Any
    nombre_completo: Optional[str] = None

class FamiliasCreate(FamiliasBase):
    pass

class FamiliasResponse(FamiliasBase):
    model_config = ConfigDict(from_attributes=True)

class JugadoresExternosBase(BaseModel):
    id: Any
    nombre_completo: Optional[str] = None

class JugadoresExternosCreate(JugadoresExternosBase):
    pass

class JugadoresExternosResponse(JugadoresExternosBase):
    model_config = ConfigDict(from_attributes=True)

class EventosBase(BaseModel):
    id: Any
    fecha: Optional[date] = None
    tipo: Optional[str] = None

class EventosCreate(EventosBase):
    pass

class EventosResponse(EventosBase):
    model_config = ConfigDict(from_attributes=True)

class PartidosBase(BaseModel):
    id: Any
    marcador_local: Optional[float] = None
    marcador_visitante: Optional[float] = None
    Rival: Optional[Any] = None
    Evento: Optional[Any] = None

class PartidosCreate(PartidosBase):
    pass

class PartidosResponse(PartidosBase):
    model_config = ConfigDict(from_attributes=True)

class PartidosExternosBase(BaseModel):
    id: Any
    equipo_local: Optional[str] = None
    equipo_visitante: Optional[str] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None

class PartidosExternosCreate(PartidosExternosBase):
    pass

class PartidosExternosResponse(PartidosExternosBase):
    model_config = ConfigDict(from_attributes=True)

class ConvocatoriaBase(BaseModel):
    id: Any
    partido: Optional[Any] = None
    jugador: Optional[Any] = None
    numero: Optional[float] = None

class ConvocatoriaCreate(ConvocatoriaBase):
    pass

class ConvocatoriaResponse(ConvocatoriaBase):
    model_config = ConfigDict(from_attributes=True)

class JugadorFamiliaBase(BaseModel):
    id_jugador_hospi: Any
    id_familia: Optional[Any] = None

class JugadorFamiliaCreate(JugadorFamiliaBase):
    pass

class JugadorFamiliaResponse(JugadorFamiliaBase):
    model_config = ConfigDict(from_attributes=True)

class EstadisticasJugadorBase(BaseModel):
    id: Any
    partido: Optional[Any] = None
    jugador: Optional[Any] = None
    ensayos: Optional[int] = None
    tarjetas_amarillas: Optional[int] = None
    tarjetas_rojas: Optional[int] = None
    nombre: Optional[str] = None
    equipo: Optional[str] = None

class EstadisticasJugadorCreate(EstadisticasJugadorBase):
    pass

class EstadisticasJugadorResponse(EstadisticasJugadorBase):
    model_config = ConfigDict(from_attributes=True)

class AnalisisPartidoBase(BaseModel):
    id: Any
    partido: Optional[Any] = Field(None, validation_alias="partido_id")
    evento: Optional[Any] = Field(None, validation_alias="evento_id")
    partido_externo: Optional[Any] = Field(None, validation_alias="partido_externo_id")
    video_url: Optional[str] = None

class AnalisisPartidoCreate(BaseModel):
    partido_id: Optional[Any] = None
    evento_id: Optional[Any] = None

class AnalisisPartidoResponse(AnalisisPartidoBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
