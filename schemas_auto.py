from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, date, time

class AsistenciaBase(BaseModel):
    id: str
    entrenamiento_id: Optional[str] = None
    jugador_id: Optional[str] = None
    asistencia: Optional[str] = None

class AsistenciaCreate(AsistenciaBase):
    pass

class AsistenciaUpdate(AsistenciaBase):
    pass

class AsistenciaResponse(AsistenciaBase):
    class Config:
        from_attributes = True

class EstadisticasPartidoBase(BaseModel):
    fecha: Optional[date] = None
    ensayos_local: Optional[int] = None
    ensayos_visitante: Optional[int] = None
    jornada: Optional[int] = None
    acta_procesada: Optional[bool] = None
    fecha_procesado: Optional[datetime] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    partido_id: Optional[str] = None
    partido_externo_id: Optional[str] = None
    id: str

class EstadisticasPartidoCreate(EstadisticasPartidoBase):
    pass

class EstadisticasPartidoUpdate(EstadisticasPartidoBase):
    pass

class EstadisticasPartidoResponse(EstadisticasPartidoBase):
    class Config:
        from_attributes = True

class EntrenamientosBase(BaseModel):
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None
    trabajo_separado: Optional[str] = None
    id_entrenamiento: str
    evento: Optional[str] = None
    trabajo_conjunto: Optional[str] = None
    calentamiento: Optional[str] = None

class EntrenamientosCreate(EntrenamientosBase):
    pass

class EntrenamientosUpdate(EntrenamientosBase):
    pass

class EntrenamientosResponse(EntrenamientosBase):
    class Config:
        from_attributes = True

class RivalesBase(BaseModel):
    fecha_creacion: Optional[datetime] = None
    id_equipo: str
    ciudad: Optional[str] = None
    escudo: Optional[str] = None
    categoria: Optional[str] = None
    temporada: Optional[str] = None
    nombre_equipo: Optional[str] = None

class RivalesCreate(RivalesBase):
    pass

class RivalesUpdate(RivalesBase):
    pass

class RivalesResponse(RivalesBase):
    class Config:
        from_attributes = True

class StaffBase(BaseModel):
    id: str
    auth_id: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    activo: Optional[bool] = None
    fecha_alta: Optional[date] = None
    fecha_baja: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    motivo_baja: Optional[str] = None
    foto_url: Optional[str] = None
    direccion: Optional[str] = None

class StaffCreate(StaffBase):
    pass

class StaffUpdate(StaffBase):
    pass

class StaffResponse(StaffBase):
    class Config:
        from_attributes = True

class JugadoresPropiosBase(BaseModel):
    Usuario: Optional[str] = None
    fecha_registro: Optional[datetime] = None
    activo: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    Telefono: Optional[float] = None
    fecha_nacimiento: Optional[date] = None
    id: str
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    posiciones: Optional[str] = None
    talla: Optional[str] = None
    licencia: Optional[str] = None
    foto: Optional[str] = None
    email: Optional[str] = None

class JugadoresPropiosCreate(JugadoresPropiosBase):
    pass

class JugadoresPropiosUpdate(JugadoresPropiosBase):
    pass

class JugadoresPropiosResponse(JugadoresPropiosBase):
    class Config:
        from_attributes = True

class FamiliasBase(BaseModel):
    updated_at: Optional[datetime] = None
    id_usuario: str
    autorizado_recoger: Optional[bool] = None
    autorizado_urgencias: Optional[bool] = None
    created_at: Optional[datetime] = None
    id_familia: Optional[str] = None
    contacto_principal: Optional[bool] = None
    nombre_completo: Optional[str] = None
    telefono: Optional[str] = None
    parentesco: Optional[str] = None
    observaciones: Optional[str] = None

class FamiliasCreate(FamiliasBase):
    pass

class FamiliasUpdate(FamiliasBase):
    pass

class FamiliasResponse(FamiliasBase):
    class Config:
        from_attributes = True

class JugadoresExternosBase(BaseModel):
    id: str
    created_at: Optional[datetime] = None
    licencia: Optional[str] = None
    nombre_completo: Optional[str] = None
    ultimo_equipo: Optional[str] = None

class JugadoresExternosCreate(JugadoresExternosBase):
    pass

class JugadoresExternosUpdate(JugadoresExternosBase):
    pass

class JugadoresExternosResponse(JugadoresExternosBase):
    class Config:
        from_attributes = True

class EventosBase(BaseModel):
    id: str
    hora: Optional[time] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    fecha: Optional[date] = None
    tipo: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None

class EventosCreate(EventosBase):
    pass

class EventosUpdate(EventosBase):
    pass

class EventosResponse(EventosBase):
    class Config:
        from_attributes = True

class PartidosBase(BaseModel):
    id: str
    es_local: Optional[bool] = None
    ensayos_local: Optional[int] = None
    ensayos_visitante: Optional[int] = None
    jornada: Optional[int] = None
    marcador_local: Optional[float] = None
    marcador_visitante: Optional[float] = None
    Rival: Optional[str] = None
    Evento: Optional[str] = None
    lugar: Optional[str] = None
    observaciones: Optional[str] = None
    acta_url: Optional[str] = None

class PartidosCreate(PartidosBase):
    pass

class PartidosUpdate(PartidosBase):
    pass

class PartidosResponse(PartidosBase):
    class Config:
        from_attributes = True

class PartidosExternosBase(BaseModel):
    ensayos_visitante: Optional[int] = None
    fecha: Optional[date] = None
    marcador_visitante: Optional[int] = None
    ensayos_local: Optional[int] = None
    id: str
    created_at: Optional[datetime] = None
    jornada: Optional[int] = None
    marcador_local: Optional[int] = None
    equipo_local: Optional[str] = None
    equipo_visitante: Optional[str] = None
    competicion: Optional[str] = None

class PartidosExternosCreate(PartidosExternosBase):
    pass

class PartidosExternosUpdate(PartidosExternosBase):
    pass

class PartidosExternosResponse(PartidosExternosBase):
    class Config:
        from_attributes = True

class ConvocatoriaBase(BaseModel):
    id: str
    partido: Optional[str] = None
    jugador: Optional[str] = None
    numero: Optional[float] = None

class ConvocatoriaCreate(ConvocatoriaBase):
    pass

class ConvocatoriaUpdate(ConvocatoriaBase):
    pass

class ConvocatoriaResponse(ConvocatoriaBase):
    class Config:
        from_attributes = True

class JugadorFamiliaBase(BaseModel):
    updated_at: Optional[datetime] = None
    id_jugador_hospi: str
    id_familia: Optional[str] = None
    id: Optional[str] = None
    convive: Optional[bool] = None
    prioridad_contacto: Optional[int] = None
    created_at: Optional[datetime] = None
    relacion_jugador: Optional[str] = None

class JugadorFamiliaCreate(JugadorFamiliaBase):
    pass

class JugadorFamiliaUpdate(JugadorFamiliaBase):
    pass

class JugadorFamiliaResponse(JugadorFamiliaBase):
    class Config:
        from_attributes = True

class EstadisticasJugadorBase(BaseModel):
    fue_convocado: Optional[bool] = None
    partido: Optional[str] = None
    jugador: Optional[str] = None
    partido_externo: Optional[str] = None
    jugador_externo: Optional[str] = None
    id: str
    dorsal: Optional[int] = None
    ensayos: Optional[int] = None
    transformaciones: Optional[int] = None
    penales: Optional[int] = None
    drops: Optional[int] = None
    tarjetas_amarillas: Optional[int] = None
    tarjetas_rojas: Optional[int] = None
    es_capitan: Optional[bool] = None
    es_titular: Optional[bool] = None
    minutos_jugados: Optional[int] = None
    equipo: Optional[str] = None
    licencia: Optional[str] = None
    nombre: Optional[str] = None

class EstadisticasJugadorCreate(EstadisticasJugadorBase):
    pass

class EstadisticasJugadorUpdate(EstadisticasJugadorBase):
    pass

class EstadisticasJugadorResponse(EstadisticasJugadorBase):
    class Config:
        from_attributes = True

class AnalisisPartidoBase(BaseModel):
    raw_json: Optional[str] = None
    partido_id: Optional[str] = None
    id: str
    video_offset_sec: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    evento_id: Optional[str] = None
    partido_externo_id: Optional[str] = None
    video_url: Optional[str] = None

class AnalisisPartidoCreate(AnalisisPartidoBase):
    pass

class AnalisisPartidoUpdate(AnalisisPartidoBase):
    pass

class AnalisisPartidoResponse(AnalisisPartidoBase):
    class Config:
        from_attributes = True

