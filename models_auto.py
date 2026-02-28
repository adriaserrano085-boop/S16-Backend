from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Asistencia(Base):
    __tablename__ = "asistencia"
    id = Column(String, primary_key=True)
    entrenamiento_id = Column(String, ForeignKey("entrenamientos.id_entrenamiento"))
    jugador_id = Column(String, ForeignKey("jugadores_propios.id"))
    asistencia = Column(String)

    # Relaciones
    entrenamientos = relationship("Entrenamientos")
    jugadores = relationship("JugadoresPropios")

class EstadisticasPartido(Base):
    __tablename__ = "estadisticas_partido"
    fecha = Column(Date)
    ensayos_local = Column(Integer)
    ensayos_visitante = Column(Integer)
    jornada = Column(Integer)
    acta_procesada = Column(Boolean)
    fecha_procesado = Column(DateTime(timezone=True))
    marcador_local = Column(Integer)
    marcador_visitante = Column(Integer)
    partido_id = Column(String, ForeignKey("partidos.id"))
    partido_externo_id = Column(String, ForeignKey("partidos_externos.id"))
    id = Column(String, primary_key=True)

    # Advanced Metrics
    posesion_local = Column(Integer)
    posesion_visitante = Column(Integer)
    placajes_hechos_local = Column(Integer)
    placajes_hechos_visitante = Column(Integer)
    placajes_fallados_local = Column(Integer)
    placajes_fallados_visitante = Column(Integer)
    mele_ganada_local = Column(Integer)
    mele_ganada_visitante = Column(Integer)
    mele_perdida_local = Column(Integer)
    mele_perdida_visitante = Column(Integer)
    touch_ganada_local = Column(Integer)
    touch_ganada_visitante = Column(Integer)
    touch_perdida_local = Column(Integer)
    touch_perdida_visitante = Column(Integer)

    partido_ref = relationship("Partidos", back_populates="estadisticas_partido")
    partido_externo_ref = relationship("PartidosExternos", back_populates="estadisticas_partido")

class Entrenamientos(Base):
    __tablename__ = "entrenamientos"
    creado_en = Column(DateTime(timezone=True))
    actualizado_en = Column(DateTime(timezone=True))
    trabajo_separado = Column(String)
    id_entrenamiento = Column(String, primary_key=True)
    evento = Column(String, ForeignKey("eventos.id"))
    trabajo_conjunto = Column(String)
    calentamiento = Column(String)

    # Relación inversa a Eventos
    evento_ref = relationship("Eventos", back_populates="entrenamiento")
    # Relación hijas (Asistencias)
    asistencias = relationship("Asistencia", back_populates="entrenamientos")

class Rivales(Base):
    __tablename__ = "rivales"
    fecha_creacion = Column(DateTime(timezone=True))
    id_equipo = Column(String, primary_key=True)
    ciudad = Column(String)
    escudo = Column(String)
    categoria = Column(String)
    temporada = Column(String)
    nombre_equipo = Column(String)

class Staff(Base):
    __tablename__ = "Staff"
    id = Column(String, primary_key=True)
    auth_id = Column(String)
    fecha_nacimiento = Column(Date)
    activo = Column(Boolean)
    fecha_alta = Column(Date)
    fecha_baja = Column(Date)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    nombre = Column(String)
    apellidos = Column(String)
    telefono = Column(String)
    motivo_baja = Column(String)
    foto_url = Column(String)
    direccion = Column(String)

class JugadoresPropios(Base):
    __tablename__ = "jugadores_propios"
    Usuario = Column(String)
    fecha_registro = Column(DateTime(timezone=True))
    activo = Column(Boolean)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    Telefono = Column(Float)
    fecha_nacimiento = Column(Date)
    id = Column(String, primary_key=True)
    nombre = Column(String)
    apellidos = Column(String)
    posiciones = Column(String)
    talla = Column(String)
    licencia = Column(String)
    foto = Column(String)
    email = Column(String)

    estadisticas_jugador = relationship("EstadisticasJugador", back_populates="jugador_ref")

class Familias(Base):
    __tablename__ = "familias"
    updated_at = Column(DateTime(timezone=True))
    id_usuario = Column(String, primary_key=True)
    autorizado_recoger = Column(Boolean)
    autorizado_urgencias = Column(Boolean)
    created_at = Column(DateTime(timezone=True))
    id_familia = Column(String)
    contacto_principal = Column(Boolean)
    nombre_completo = Column(String)
    telefono = Column(String)
    parentesco = Column(String)
    observaciones = Column(String)

class JugadoresExternos(Base):
    __tablename__ = "jugadores_externos"
    id = Column(String, primary_key=True)
    created_at = Column(DateTime(timezone=True))
    licencia = Column(String)
    nombre_completo = Column(String)
    ultimo_equipo = Column(String)

class Eventos(Base):
    __tablename__ = "eventos"
    id = Column(String, primary_key=True)
    hora = Column(Time(timezone=True))
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    fecha = Column(Date)
    tipo = Column(String)
    estado = Column(String)
    observaciones = Column(String)

    # Relaciones hacia Partidos y Entrenamientos (uselist=False porque es 1-a-1)
    partido = relationship("Partidos", back_populates="evento_ref", uselist=False)
    entrenamiento = relationship("Entrenamientos", back_populates="evento_ref", uselist=False)
    analisis = relationship("AnalisisPartido", back_populates="evento_ref", uselist=False)

class Partidos(Base):
    __tablename__ = "partidos"
    id = Column(String, primary_key=True)
    es_local = Column(Boolean)
    ensayos_local = Column(Integer)
    ensayos_visitante = Column(Integer)
    jornada = Column(Integer)
    marcador_local = Column(Float)
    marcador_visitante = Column(Float)
    Rival = Column(String, ForeignKey("rivales.id_equipo"))
    Evento = Column(String, ForeignKey("eventos.id"))
    lugar = Column(String)
    observaciones = Column(String)
    acta_url = Column(String)

    # Relación inversa a Eventos
    evento_ref = relationship("Eventos", back_populates="partido")
    # Relación a Rivales
    rival_ref = relationship("Rivales")
    
    estadisticas_partido = relationship("EstadisticasPartido", back_populates="partido_ref")
    estadisticas_jugador = relationship("EstadisticasJugador", back_populates="partido_ref")

class PartidosExternos(Base):
    __tablename__ = "partidos_externos"
    ensayos_visitante = Column(Integer)
    fecha = Column(Date)
    marcador_visitante = Column(Integer)
    ensayos_local = Column(Integer)
    id = Column(String, primary_key=True)
    created_at = Column(DateTime(timezone=True))
    jornada = Column(Integer)
    marcador_local = Column(Integer)
    equipo_local = Column(String)
    equipo_visitante = Column(String)
    competicion = Column(String)

    estadisticas_partido = relationship("EstadisticasPartido", back_populates="partido_externo_ref")
    estadisticas_jugador = relationship("EstadisticasJugador", back_populates="partido_externo_ref")

class Convocatoria(Base):
    __tablename__ = "convocatoria"
    id = Column(String, primary_key=True)
    partido = Column(String)
    jugador = Column(String)
    numero = Column(Float)

class JugadorFamilia(Base):
    __tablename__ = "jugador_familia"
    updated_at = Column(DateTime(timezone=True))
    id_jugador_hospi = Column(String, primary_key=True)
    id_familia = Column(String)
    id = Column(String)
    convive = Column(Boolean)
    prioridad_contacto = Column(Integer)
    created_at = Column(DateTime(timezone=True))
    relacion_jugador = Column(String)

class EstadisticasJugador(Base):
    __tablename__ = "estadisticas_jugador"
    fue_convocado = Column(Boolean)
    partido = Column(String, ForeignKey("partidos.id"))
    jugador = Column(String, ForeignKey("jugadores_propios.id"))
    partido_externo = Column(String, ForeignKey("partidos_externos.id"))
    jugador_externo = Column(String)
    id = Column(String, primary_key=True)
    dorsal = Column(Integer)
    ensayos = Column(Integer)
    transformaciones = Column(Integer)
    penales = Column(Integer)
    drops = Column(Integer)
    tarjetas_amarillas = Column(Integer)
    tarjetas_rojas = Column(Integer)
    es_capitan = Column(Boolean)
    es_titular = Column(Boolean)
    minutos_jugados = Column(Integer)
    equipo = Column(String)
    licencia = Column(String)
    nombre = Column(String)

    partido_ref = relationship("Partidos", back_populates="estadisticas_jugador")
    partido_externo_ref = relationship("PartidosExternos", back_populates="estadisticas_jugador")
    jugador_ref = relationship("JugadoresPropios", back_populates="estadisticas_jugador")

class AnalisisPartido(Base):
    __tablename__ = "analisis_partido"
    raw_json = Column(String)
    partido_id = Column(String, ForeignKey("partidos.id"))
    id = Column(String, primary_key=True)
    video_offset_sec = Column(Integer)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    evento_id = Column(String, ForeignKey("eventos.id"))
    partido_externo_id = Column(String, ForeignKey("partidos_externos.id"))
    video_url = Column(String)
    
    evento_ref = relationship("Eventos", back_populates="analisis")

