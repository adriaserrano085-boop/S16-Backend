from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date
import models_auto as models
import schemas_auto as schemas
from database import get_db

router = APIRouter()

# --- CRUD for Asistencia ---
@router.get("/asistencia", response_model=List[schemas.AsistenciaResponse], tags=["Asistencia"])
def read_asistencia_list(
    skip: int = 0, 
    limit: int = 10000, 
    entrenamiento: Optional[str] = None,
    jugador: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Asistencia).options(
        joinedload(models.Asistencia.entrenamientos),
        joinedload(models.Asistencia.jugadores)
    )
    if entrenamiento:
        query = query.filter(models.Asistencia.entrenamiento_id == entrenamiento)
    if jugador:
        query = query.filter(models.Asistencia.jugador_id == jugador)
    return query.offset(skip).limit(limit).all()

@router.get("/asistencia/{item_id}", response_model=schemas.AsistenciaResponse, tags=["Asistencia"])
def read_asistencia(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Asistencia).filter(models.Asistencia.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/asistencia", response_model=schemas.AsistenciaResponse, tags=["Asistencia"])
def create_asistencia(item: schemas.AsistenciaCreate, db: Session = Depends(get_db)):
    # Duplicate check
    existing = db.query(models.Asistencia).filter(
        models.Asistencia.entrenamiento_id == item.entrenamiento_id,
        models.Asistencia.jugador_id == item.jugador_id
    ).first()
    if existing:
        existing.asistencia = item.asistencia
        db.commit()
        db.refresh(existing)
        return existing

    db_item = models.Asistencia(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- CRUD for EstadisticasPartido ---
@router.get("/estadisticas_partido", response_model=List[schemas.EstadisticasPartidoResponse], tags=["EstadisticasPartido"])
def read_estadisticas_partido_list(
    skip: int = 0, 
    limit: int = 10000, 
    partido: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.EstadisticasPartido)
    if partido:
        query = query.filter(models.EstadisticasPartido.partido_id == partido)
    return query.offset(skip).limit(limit).all()

# --- CRUD for Entrenamientos ---
@router.get("/entrenamientos", response_model=List[schemas.EntrenamientosDetalleResponse], tags=["Entrenamientos"])
def read_entrenamientos_list(
    skip: int = 0, 
    limit: int = 10000, 
    evento: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Entrenamientos).options(
        joinedload(models.Entrenamientos.evento_ref),
        joinedload(models.Entrenamientos.asistencias)
    )
    if evento:
        query = query.filter(models.Entrenamientos.evento == evento)
    return query.offset(skip).limit(limit).all()

@router.get("/entrenamientos/{item_id}", response_model=schemas.EntrenamientosDetalleResponse, tags=["Entrenamientos"])
def read_entrenamientos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Entrenamientos).options(
        joinedload(models.Entrenamientos.evento_ref),
        joinedload(models.Entrenamientos.asistencias)
    ).filter(models.Entrenamientos.id_entrenamiento == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

# --- CRUD for Rivales ---
@router.get("/rivales", response_model=List[schemas.RivalesResponse], tags=["Rivales"])
def read_rivales_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Rivales).offset(skip).limit(limit).all()

@router.get("/rivales/{item_id}", response_model=schemas.RivalesResponse, tags=["Rivales"])
def read_rivales(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Rivales).filter(models.Rivales.id_equipo == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

# --- CRUD for JugadoresPropios ---
@router.get("/jugadores_propios", response_model=List[schemas.JugadoresPropiosResponse], tags=["JugadoresPropios"])
def read_jugadores_propios_list(
    skip: int = 0, 
    limit: int = 100, 
    email: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.JugadoresPropios)
    if email:
        query = query.filter(models.JugadoresPropios.email == email)
    return query.offset(skip).limit(limit).all()

# --- CRUD for Eventos ---
@router.get("/eventos", response_model=List[schemas.EventosResponse], tags=["Eventos"])
def read_eventos_list(
    skip: int = 0, 
    limit: int = 10000, 
    tipo: Optional[str] = None,
    fecha: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Eventos).options(
        joinedload(models.Eventos.partido),
        joinedload(models.Eventos.entrenamiento),
        joinedload(models.Eventos.analisis)
    )
    if tipo:
        query = query.filter(models.Eventos.tipo == tipo)
    if fecha:
        query = query.filter(models.Eventos.fecha == fecha)
    return query.offset(skip).limit(limit).all()

# --- CRUD for JugadoresExternos ---
@router.get("/jugadores_externos/", response_model=List[schemas.JugadoresExternosResponse], tags=["JugadoresExternos"])
@router.get("/jugadores_externos", response_model=List[schemas.JugadoresExternosResponse], tags=["JugadoresExternos"])
def read_jugadores_externos_list(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    return db.query(models.JugadoresExternos).offset(skip).limit(limit).all()

@router.post("/jugadores_externos/", response_model=schemas.JugadoresExternosResponse, tags=["JugadoresExternos"])
@router.post("/jugadores_externos", response_model=schemas.JugadoresExternosResponse, tags=["JugadoresExternos"])
def create_jugador_externo(item: schemas.JugadoresExternosCreate, db: Session = Depends(get_db)):
    # Duplicate check by licencia
    if item.licencia:
        existing = db.query(models.JugadoresExternos).filter(models.JugadoresExternos.licencia == item.licencia).first()
        if existing:
            # Update existing
            existing.nombre_completo = item.nombre_completo
            existing.ultimo_equipo = item.ultimo_equipo
            db.commit()
            db.refresh(existing)
            return existing
    
    db_item = models.JugadoresExternos(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- CRUD for Partidos ---
@router.get("/partidos", response_model=List[schemas.PartidosResponse], tags=["Partidos"])
def read_partidos_list(
    skip: int = 0, 
    limit: int = 10000, 
    rival: Optional[str] = None,
    evento: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Partidos).options(
        joinedload(models.Partidos.estadisticas_partido),
        joinedload(models.Partidos.estadisticas_jugador)
    )
    if rival:
        query = query.filter(models.Partidos.Rival == rival)
    if evento:
        query = query.filter(models.Partidos.Evento == evento)
    return query.offset(skip).limit(limit).all()

@router.get("/partidos/{item_id}", response_model=schemas.PartidosResponse, tags=["Partidos"])
def read_partido(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Partidos).options(
        joinedload(models.Partidos.estadisticas_partido),
        joinedload(models.Partidos.estadisticas_jugador)
    ).filter(models.Partidos.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Partido not found")
    return item

@router.put("/partidos/{item_id}", response_model=schemas.PartidosResponse, tags=["Partidos"])
def update_partido(item_id: str, obj_in: schemas.PartidosUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(models.Partidos).filter(models.Partidos.id == item_id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Partido not found")
    
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# --- CRUD for PartidosExternos ---
@router.get("/partidos_externos", response_model=List[schemas.PartidosExternosResponse], tags=["PartidosExternos"])
def read_partidos_externos_list(
    skip: int = 0, 
    limit: int = 100, 
    fecha: Optional[date] = None,
    equipo_local: Optional[str] = None,
    equipo_visitante: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.PartidosExternos).options(
        joinedload(models.PartidosExternos.estadisticas_partido),
        joinedload(models.PartidosExternos.estadisticas_jugador)
    )
    if fecha:
        query = query.filter(models.PartidosExternos.fecha == fecha)
    if equipo_local:
        query = query.filter(models.PartidosExternos.equipo_local == equipo_local)
    if equipo_visitante:
        query = query.filter(models.PartidosExternos.equipo_visitante == equipo_visitante)
    return query.offset(skip).limit(limit).all()

@router.post("/partidos_externos", response_model=schemas.PartidosExternosResponse, tags=["PartidosExternos"])
def create_partido_externo(obj_in: schemas.PartidosExternosCreate, db: Session = Depends(get_db)):
    obj_data = obj_in.model_dump()
    
    # Upsert logic: check by date and teams
    existing = db.query(models.PartidosExternos).filter(
        models.PartidosExternos.fecha == obj_data["fecha"],
        models.PartidosExternos.equipo_local == obj_data["equipo_local"],
        models.PartidosExternos.equipo_visitante == obj_data["equipo_visitante"]
    ).first()
    
    if existing:
        for field, value in obj_data.items():
            if field != "id":
                setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing

    db_obj = models.PartidosExternos(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.put("/partidos_externos/{item_id}", response_model=schemas.PartidosExternosResponse, tags=["PartidosExternos"])
def update_partido_externo(item_id: str, obj_in: schemas.PartidosExternosBase, db: Session = Depends(get_db)):
    db_obj = db.query(models.PartidosExternos).filter(models.PartidosExternos.id == item_id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="PartidoExterno not found")
    
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/partidos_externos/{item_id}", tags=["PartidosExternos"])
def delete_partido_externo(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.PartidosExternos).filter(models.PartidosExternos.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for EstadisticasJugador ---
@router.get("/estadisticas_jugador/", response_model=List[schemas.EstadisticasJugadorResponse], tags=["EstadisticasJugador"])
@router.get("/estadisticas_jugador", response_model=List[schemas.EstadisticasJugadorResponse], tags=["EstadisticasJugador"])
def read_estadisticas_jugador_list(
    skip: int = 0, 
    limit: int = 10000, 
    partido: Optional[str] = None,
    partido_externo: Optional[str] = None,
    jugador: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.EstadisticasJugador)
    if partido:
        query = query.filter(models.EstadisticasJugador.partido == partido)
    if partido_externo:
        query = query.filter(models.EstadisticasJugador.partido_externo == partido_externo)
    if jugador:
        query = query.filter(models.EstadisticasJugador.jugador == jugador)
    return query.offset(skip).limit(limit).all()

@router.get("/estadisticas_jugador/{item_id}", response_model=schemas.EstadisticasJugadorResponse, tags=["EstadisticasJugador"])
def read_estadisticas_jugador(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.EstadisticasJugador).filter(models.EstadisticasJugador.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/estadisticas_jugador", response_model=schemas.EstadisticasJugadorResponse, tags=["EstadisticasJugador"])
def create_estadisticas_jugador(obj_in: schemas.EstadisticasJugadorCreate, db: Session = Depends(get_db)):
    obj_data = obj_in.model_dump()
    
    # Duplicate check logic
    query = db.query(models.EstadisticasJugador)
    if obj_data.get("partido"):
        query = query.filter(models.EstadisticasJugador.partido == obj_data["partido"])
    elif obj_data.get("partido_externo"):
        query = query.filter(models.EstadisticasJugador.partido_externo == obj_data["partido_externo"])
    
    if obj_data.get("jugador"):
        query = query.filter(models.EstadisticasJugador.jugador == obj_data["jugador"])
    elif obj_data.get("jugador_externo"):
        query = query.filter(models.EstadisticasJugador.jugador_externo == obj_data["jugador_externo"])
    elif obj_data.get("licencia"):
        query = query.filter(models.EstadisticasJugador.licencia == obj_data["licencia"])
    else:
        query = query.filter(models.EstadisticasJugador.nombre == obj_data["nombre"])
    
    existing = query.first()
    if existing:
        for field, value in obj_data.items():
            if field != "id":
                setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing

    db_obj = models.EstadisticasJugador(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/estadisticas_jugador/{item_id}", tags=["EstadisticasJugador"])
def delete_estadisticas_jugador_by_id(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.EstadisticasJugador).filter(models.EstadisticasJugador.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

@router.delete("/estadisticas_jugador", tags=["EstadisticasJugador"])
def delete_estadisticas_jugador(
    partido: Optional[str] = None,
    partido_externo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if not partido and not partido_externo:
        raise HTTPException(status_code=400, detail="Must provide partido or partido_externo")
    
    query = db.query(models.EstadisticasJugador)
    if partido:
        query = query.filter(models.EstadisticasJugador.partido == partido)
    if partido_externo:
        query = query.filter(models.EstadisticasJugador.partido_externo == partido_externo)
    
    deleted_count = query.delete()
    db.commit()
    return {"message": f"Deleted {deleted_count} records"}

# --- analísis_partido METHODS ---
@router.get("/analisis_partido", response_model=List[schemas.AnalisisPartidoResponse], tags=["AnalisisPartido"])
def read_analisis_partido_list(
    skip: int = 0, 
    limit: int = 1000, 
    partido: Optional[str] = None,
    partido_externo: Optional[str] = None,
    evento: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.AnalisisPartido)
    if partido:
        query = query.filter(models.AnalisisPartido.partido_id == partido)
    if partido_externo:
        query = query.filter(models.AnalisisPartido.partido_externo_id == partido_externo)
    if evento:
        query = query.filter(models.AnalisisPartido.evento_id == evento)
    return query.offset(skip).limit(limit).all()

@router.post("/analisis_partido", response_model=schemas.AnalisisPartidoResponse, tags=["AnalisisPartido"])
def create_analisis_partido(obj_in: schemas.AnalisisPartidoCreate, db: Session = Depends(get_db)):
    import json
    obj_data = obj_in.model_dump()
    
    query = db.query(models.AnalisisPartido)
    if obj_data.get("partido_id"):
        query = query.filter(models.AnalisisPartido.partido_id == obj_data["partido_id"])
    elif obj_data.get("partido_externo_id"):
        query = query.filter(models.AnalisisPartido.partido_externo_id == obj_data["partido_externo_id"])
    
    existing = query.first()
    if obj_data.get("raw_json") is not None and not isinstance(obj_data["raw_json"], str):
        obj_data["raw_json"] = json.dumps(obj_data["raw_json"])
        
    if existing:
        for field, value in obj_data.items():
            if field != "id":
                setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing

    db_obj = models.AnalisisPartido(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.put("/analisis_partido/{item_id}", response_model=schemas.AnalisisPartidoResponse, tags=["AnalisisPartido"])
def update_analisis_partido(item_id: str, obj_in: schemas.AnalisisPartidoUpdate, db: Session = Depends(get_db)):
    import json
    db_obj = db.query(models.AnalisisPartido).filter(models.AnalisisPartido.id == item_id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Analisis not found")
    
    update_data = obj_in.model_dump(exclude_unset=True)
    if update_data.get("raw_json") is not None and not isinstance(update_data["raw_json"], str):
        update_data["raw_json"] = json.dumps(update_data["raw_json"])
        
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# --- estadisticas_partido METHODS ---
@router.get("/estadisticas_partido/{item_id}", response_model=schemas.EstadisticasPartidoResponse, tags=["EstadisticasPartido"])
def read_estadisticas_partido(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.EstadisticasPartido).filter(models.EstadisticasPartido.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/estadisticas_partido", response_model=schemas.EstadisticasPartidoResponse, tags=["EstadisticasPartido"])
def create_estadisticas_partido(obj_in: schemas.EstadisticasPartidoCreate, db: Session = Depends(get_db)):
    obj_data = obj_in.model_dump()
    
    query = db.query(models.EstadisticasPartido)
    if obj_data.get("partido_id"):
        query = query.filter(models.EstadisticasPartido.partido_id == obj_data["partido_id"])
    elif obj_data.get("partido_externo_id"):
        query = query.filter(models.EstadisticasPartido.partido_externo_id == obj_data["partido_externo_id"])
    
    existing = query.first()
    if existing:
        for field, value in obj_data.items():
            if field != "id":
                setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing

    db_obj = models.EstadisticasPartido(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/estadisticas_partido/{item_id}", tags=["EstadisticasPartido"])
def delete_estadisticas_partido_by_id(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.EstadisticasPartido).filter(models.EstadisticasPartido.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

@router.post("/borrar_datos_partido", tags=["CustomOps"])
def borrar_datos_partido(payload: dict, db: Session = Depends(get_db)):
    match_id = payload.get("match_id")
    match_type = payload.get("type")
    
    if not match_id or not match_type:
        raise HTTPException(status_code=400, detail="Missing match_id or type")

    if match_type == 'standard':
        db.query(models.EstadisticasJugador).filter(models.EstadisticasJugador.partido == match_id).delete()
        db.query(models.EstadisticasPartido).filter(models.EstadisticasPartido.partido_id == match_id).delete()
        db.query(models.AnalisisPartido).filter(models.AnalisisPartido.partido_id == match_id).delete()
        
        partido = db.query(models.Partidos).filter(models.Partidos.id == match_id).first()
        if partido:
            partido.marcador_local = None
            partido.marcador_visitante = None
            partido.ensayos_local = 0
            partido.ensayos_visitante = 0
            partido.acta_url = None
            
    elif match_type == 'external':
        db.query(models.EstadisticasJugador).filter(models.EstadisticasJugador.partido_externo == match_id).delete()
        db.query(models.EstadisticasPartido).filter(models.EstadisticasPartido.partido_externo_id == match_id).delete()
        db.query(models.AnalisisPartido).filter(models.AnalisisPartido.partido_externo_id == match_id).delete()
        db.query(models.PartidosExternos).filter(models.PartidosExternos.id == match_id).delete()
    
    db.commit()
    return {"message": "Match data deleted/reset successfully"}

@router.put("/estadisticas_partido/{item_id}", response_model=schemas.EstadisticasPartidoResponse, tags=["EstadisticasPartido"])
def update_estadisticas_partido(item_id: str, obj_in: schemas.EstadisticasPartidoUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(models.EstadisticasPartido).filter(models.EstadisticasPartido.id == item_id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/estadisticas_partido", tags=["EstadisticasPartido"])
def delete_estadisticas_partido(
    partido: Optional[str] = None,
    partido_externo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if not partido and not partido_externo:
        raise HTTPException(status_code=400, detail="Must provide partido or partido_externo")
    
    query = db.query(models.EstadisticasPartido)
    if partido:
        query = query.filter(models.EstadisticasPartido.partido_id == partido)
    if partido_externo:
        query = query.filter(models.EstadisticasPartido.partido_externo_id == partido_externo)
    
    deleted_count = query.delete()
    db.commit()
    return {"message": f"Deleted {deleted_count} records"}

@router.delete("/asistencia/{item_id}", tags=["Asistencia"])
def delete_asistencia(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Asistencia).filter(models.Asistencia.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

@router.post("/crear_o_actualizar_evento", tags=["CustomOps"])
def crear_o_actualizar_evento(obj_in: schemas.EventoCreateUpdate, db: Session = Depends(get_db)):
    import uuid
    
    # 1. Handle Evento (Base)
    evento_id = obj_in.id
    db_evento = None
    
    if evento_id:
        db_evento = db.query(models.Eventos).filter(models.Eventos.id == evento_id).first()
    
    if db_evento:
        # Update existing
        db_evento.tipo = obj_in.tipo
        db_evento.fecha = obj_in.fecha
        db_evento.hora = obj_in.hora
        db_evento.lugar = obj_in.lugar
        db_evento.estado = obj_in.estado
        db_evento.observaciones = obj_in.observaciones
    else:
        # Create new
        new_id = str(uuid.uuid4())
        db_evento = models.Eventos(
            id=new_id,
            tipo=obj_in.tipo,
            fecha=obj_in.fecha,
            hora=obj_in.hora,
            lugar=obj_in.lugar,
            estado=obj_in.estado,
            observaciones=obj_in.observaciones
        )
        db.add(db_evento)
    
    db.flush() # Get the ID if new
    actual_evento_id = db_evento.id

    # 2. Handle Specific Data (Partido or Entrenamiento)
    if obj_in.tipo == 'Partido':
        # Check if Partidos entry exists for this event
        db_partido = db.query(models.Partidos).filter(models.Partidos.evento_id == actual_evento_id).first()
        
        if db_partido:
            db_partido.rival_id = obj_in.rival_id
            db_partido.es_local = obj_in.es_local
            db_partido.marcador_local = obj_in.marcador_local
            db_partido.marcador_visitante = obj_in.marcador_visitante
        else:
            new_partido = models.Partidos(
                id=str(uuid.uuid4()),
                evento_id=actual_evento_id,
                rival_id=obj_in.rival_id,
                es_local=obj_in.es_local,
                marcador_local=obj_in.marcador_local,
                marcador_visitante=obj_in.marcador_visitante
            )
            db.add(new_partido)
            
    elif obj_in.tipo == 'Entrenamiento':
        # Check if Entrenamientos entry exists for this event
        db_entrenamiento = db.query(models.Entrenamientos).filter(models.Entrenamientos.evento_id == actual_evento_id).first()
        
        if db_entrenamiento:
            db_entrenamiento.calentamiento = obj_in.calentamiento
            db_entrenamiento.trabajo_separado = obj_in.trabajo_separado
            db_entrenamiento.trabajo_conjunto = obj_in.trabajo_conjunto
        else:
            new_entrenamiento = models.Entrenamientos(
                id=str(uuid.uuid4()),
                evento_id=actual_evento_id,
                calentamiento=obj_in.calentamiento,
                trabajo_separado=obj_in.trabajo_separado,
                trabajo_conjunto=obj_in.trabajo_conjunto
            )
            db.add(new_entrenamiento)

    db.commit()
    db.refresh(db_evento)
    return db_evento
