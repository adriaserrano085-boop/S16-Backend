from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
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
    db_item = models.Asistencia(**item.model_dump())
    import uuid
    if not db_item.id: db_item.id = str(uuid.uuid4())
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
    db: Session = Depends(get_db)
):
    query = db.query(models.Eventos).options(
        joinedload(models.Eventos.partido),
        joinedload(models.Eventos.entrenamiento),
        joinedload(models.Eventos.analisis)
    )
    if tipo:
        query = query.filter(models.Eventos.tipo == tipo)
    return query.offset(skip).limit(limit).all()

# --- CRUD for JugadoresExternos ---
@router.get("/jugadores_externos/", response_model=List[schemas.JugadoresExternosResponse], tags=["JugadoresExternos"])
@router.get("/jugadores_externos", response_model=List[schemas.JugadoresExternosResponse], tags=["JugadoresExternos"])
def read_jugadores_externos_list(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    return db.query(models.JugadoresExternos).offset(skip).limit(limit).all()

@router.post("/jugadores_externos/", response_model=schemas.JugadoresExternosResponse, tags=["JugadoresExternos"])
@router.post("/jugadores_externos", response_model=schemas.JugadoresExternosResponse, tags=["JugadoresExternos"])
def create_jugador_externo(item: schemas.JugadoresExternosCreate, db: Session = Depends(get_db)):
    import uuid
    db_item = models.JugadoresExternos(**item.model_dump())
    if not db_item.id: db_item.id = str(uuid.uuid4())
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
def read_partidos_externos_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(models.PartidosExternos).options(
        joinedload(models.PartidosExternos.estadisticas_partido),
        joinedload(models.PartidosExternos.estadisticas_jugador)
    )
    return query.offset(skip).limit(limit).all()

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
def create_estadisticas_jugador(obj_in: schemas.EstadisticasJugadorBase, db: Session = Depends(get_db)):
    import uuid
    obj_data = obj_in.model_dump()
    if not obj_data.get("id"):
        obj_data["id"] = str(uuid.uuid4())
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
    import uuid
    import json
    
    obj_data = obj_in.model_dump()
    if not obj_data.get("id"):
        obj_data["id"] = str(uuid.uuid4())
    
    # Handle raw_json if it's a dict/list
    if obj_data.get("raw_json") is not None and not isinstance(obj_data["raw_json"], str):
        obj_data["raw_json"] = json.dumps(obj_data["raw_json"])
        
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
    import uuid
    obj_data = obj_in.model_dump()
    if not obj_data.get("id"):
        obj_data["id"] = str(uuid.uuid4())
    db_obj = models.EstadisticasPartido(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

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
