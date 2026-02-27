from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models_auto as models
import schemas_auto as schemas
from database import get_db

router = APIRouter()

# --- CRUD for Asistencia ---
@router.get("/asistencia/", response_model=List[schemas.AsistenciaResponse], tags=["Asistencia"])
def read_asistencia_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Asistencia).offset(skip).limit(limit).all()

@router.get("/asistencia/{item_id}", response_model=schemas.AsistenciaResponse, tags=["Asistencia"])
def read_asistencia(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Asistencia).filter(models.Asistencia.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/asistencia/", response_model=schemas.AsistenciaResponse, tags=["Asistencia"])
def create_asistencia(item: schemas.AsistenciaCreate, db: Session = Depends(get_db)):
    db_item = models.Asistencia(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/asistencia/{item_id}", tags=["Asistencia"])
def delete_asistencia(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Asistencia).filter(models.Asistencia.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for EstadisticasPartido ---
@router.get("/estadisticas_partido/", response_model=List[schemas.EstadisticasPartidoResponse], tags=["EstadisticasPartido"])
def read_estadisticas_partido_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.EstadisticasPartido).offset(skip).limit(limit).all()

@router.get("/estadisticas_partido/{item_id}", response_model=schemas.EstadisticasPartidoResponse, tags=["EstadisticasPartido"])
def read_estadisticas_partido(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.EstadisticasPartido).filter(models.EstadisticasPartido.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/estadisticas_partido/", response_model=schemas.EstadisticasPartidoResponse, tags=["EstadisticasPartido"])
def create_estadisticas_partido(item: schemas.EstadisticasPartidoCreate, db: Session = Depends(get_db)):
    db_item = models.EstadisticasPartido(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/estadisticas_partido/{item_id}", tags=["EstadisticasPartido"])
def delete_estadisticas_partido(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.EstadisticasPartido).filter(models.EstadisticasPartido.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for Entrenamientos ---
@router.get("/entrenamientos/", response_model=List[schemas.EntrenamientosResponse], tags=["Entrenamientos"])
def read_entrenamientos_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Entrenamientos).offset(skip).limit(limit).all()

@router.get("/entrenamientos/{item_id}", response_model=schemas.EntrenamientosResponse, tags=["Entrenamientos"])
def read_entrenamientos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Entrenamientos).filter(models.Entrenamientos.id_entrenamiento == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/entrenamientos/", response_model=schemas.EntrenamientosResponse, tags=["Entrenamientos"])
def create_entrenamientos(item: schemas.EntrenamientosCreate, db: Session = Depends(get_db)):
    db_item = models.Entrenamientos(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/entrenamientos/{item_id}", tags=["Entrenamientos"])
def delete_entrenamientos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Entrenamientos).filter(models.Entrenamientos.id_entrenamiento == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for Rivales ---
@router.get("/rivales/", response_model=List[schemas.RivalesResponse], tags=["Rivales"])
def read_rivales_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Rivales).offset(skip).limit(limit).all()

@router.get("/rivales/{item_id}", response_model=schemas.RivalesResponse, tags=["Rivales"])
def read_rivales(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Rivales).filter(models.Rivales.id_equipo == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/rivales/", response_model=schemas.RivalesResponse, tags=["Rivales"])
def create_rivales(item: schemas.RivalesCreate, db: Session = Depends(get_db)):
    db_item = models.Rivales(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/rivales/{item_id}", tags=["Rivales"])
def delete_rivales(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Rivales).filter(models.Rivales.id_equipo == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for Staff ---
@router.get("/Staff/", response_model=List[schemas.StaffResponse], tags=["Staff"])
def read_staff_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Staff).offset(skip).limit(limit).all()

@router.get("/Staff/{item_id}", response_model=schemas.StaffResponse, tags=["Staff"])
def read_staff(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Staff).filter(models.Staff.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/Staff/", response_model=schemas.StaffResponse, tags=["Staff"])
def create_staff(item: schemas.StaffCreate, db: Session = Depends(get_db)):
    db_item = models.Staff(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/Staff/{item_id}", tags=["Staff"])
def delete_staff(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Staff).filter(models.Staff.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for JugadoresPropios ---
@router.get("/jugadores_propios/", response_model=List[schemas.JugadoresPropiosResponse], tags=["JugadoresPropios"])
def read_jugadores_propios_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.JugadoresPropios).offset(skip).limit(limit).all()

@router.get("/jugadores_propios/{item_id}", response_model=schemas.JugadoresPropiosResponse, tags=["JugadoresPropios"])
def read_jugadores_propios(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.JugadoresPropios).filter(models.JugadoresPropios.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/jugadores_propios/", response_model=schemas.JugadoresPropiosResponse, tags=["JugadoresPropios"])
def create_jugadores_propios(item: schemas.JugadoresPropiosCreate, db: Session = Depends(get_db)):
    db_item = models.JugadoresPropios(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/jugadores_propios/{item_id}", tags=["JugadoresPropios"])
def delete_jugadores_propios(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.JugadoresPropios).filter(models.JugadoresPropios.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for Familias ---
@router.get("/familias/", response_model=List[schemas.FamiliasResponse], tags=["Familias"])
def read_familias_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Familias).offset(skip).limit(limit).all()

@router.get("/familias/{item_id}", response_model=schemas.FamiliasResponse, tags=["Familias"])
def read_familias(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Familias).filter(models.Familias.id_usuario == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/familias/", response_model=schemas.FamiliasResponse, tags=["Familias"])
def create_familias(item: schemas.FamiliasCreate, db: Session = Depends(get_db)):
    db_item = models.Familias(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/familias/{item_id}", tags=["Familias"])
def delete_familias(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Familias).filter(models.Familias.id_usuario == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for JugadoresExternos ---
@router.get("/jugadores_externos/", response_model=List[schemas.JugadoresExternosResponse], tags=["JugadoresExternos"])
def read_jugadores_externos_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.JugadoresExternos).offset(skip).limit(limit).all()

@router.get("/jugadores_externos/{item_id}", response_model=schemas.JugadoresExternosResponse, tags=["JugadoresExternos"])
def read_jugadores_externos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.JugadoresExternos).filter(models.JugadoresExternos.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/jugadores_externos/", response_model=schemas.JugadoresExternosResponse, tags=["JugadoresExternos"])
def create_jugadores_externos(item: schemas.JugadoresExternosCreate, db: Session = Depends(get_db)):
    db_item = models.JugadoresExternos(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/jugadores_externos/{item_id}", tags=["JugadoresExternos"])
def delete_jugadores_externos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.JugadoresExternos).filter(models.JugadoresExternos.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for Eventos ---
@router.get("/eventos/", response_model=List[schemas.EventosResponse], tags=["Eventos"])
def read_eventos_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Eventos).offset(skip).limit(limit).all()

@router.get("/eventos/{item_id}", response_model=schemas.EventosResponse, tags=["Eventos"])
def read_eventos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Eventos).filter(models.Eventos.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/eventos/", response_model=schemas.EventosResponse, tags=["Eventos"])
def create_eventos(item: schemas.EventosCreate, db: Session = Depends(get_db)):
    db_item = models.Eventos(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/eventos/{item_id}", tags=["Eventos"])
def delete_eventos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Eventos).filter(models.Eventos.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for Partidos ---
@router.get("/partidos/", response_model=List[schemas.PartidosResponse], tags=["Partidos"])
def read_partidos_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Partidos).offset(skip).limit(limit).all()

@router.get("/partidos/{item_id}", response_model=schemas.PartidosResponse, tags=["Partidos"])
def read_partidos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Partidos).filter(models.Partidos.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/partidos/", response_model=schemas.PartidosResponse, tags=["Partidos"])
def create_partidos(item: schemas.PartidosCreate, db: Session = Depends(get_db)):
    db_item = models.Partidos(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/partidos/{item_id}", tags=["Partidos"])
def delete_partidos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Partidos).filter(models.Partidos.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for PartidosExternos ---
@router.get("/partidos_externos/", response_model=List[schemas.PartidosExternosResponse], tags=["PartidosExternos"])
def read_partidos_externos_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.PartidosExternos).offset(skip).limit(limit).all()

@router.get("/partidos_externos/{item_id}", response_model=schemas.PartidosExternosResponse, tags=["PartidosExternos"])
def read_partidos_externos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.PartidosExternos).filter(models.PartidosExternos.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/partidos_externos/", response_model=schemas.PartidosExternosResponse, tags=["PartidosExternos"])
def create_partidos_externos(item: schemas.PartidosExternosCreate, db: Session = Depends(get_db)):
    db_item = models.PartidosExternos(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/partidos_externos/{item_id}", tags=["PartidosExternos"])
def delete_partidos_externos(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.PartidosExternos).filter(models.PartidosExternos.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for Convocatoria ---
@router.get("/convocatoria/", response_model=List[schemas.ConvocatoriaResponse], tags=["Convocatoria"])
def read_convocatoria_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Convocatoria).offset(skip).limit(limit).all()

@router.get("/convocatoria/{item_id}", response_model=schemas.ConvocatoriaResponse, tags=["Convocatoria"])
def read_convocatoria(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Convocatoria).filter(models.Convocatoria.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/convocatoria/", response_model=schemas.ConvocatoriaResponse, tags=["Convocatoria"])
def create_convocatoria(item: schemas.ConvocatoriaCreate, db: Session = Depends(get_db)):
    db_item = models.Convocatoria(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/convocatoria/{item_id}", tags=["Convocatoria"])
def delete_convocatoria(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Convocatoria).filter(models.Convocatoria.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for JugadorFamilia ---
@router.get("/jugador_familia/", response_model=List[schemas.JugadorFamiliaResponse], tags=["JugadorFamilia"])
def read_jugador_familia_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.JugadorFamilia).offset(skip).limit(limit).all()

@router.get("/jugador_familia/{item_id}", response_model=schemas.JugadorFamiliaResponse, tags=["JugadorFamilia"])
def read_jugador_familia(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.JugadorFamilia).filter(models.JugadorFamilia.id_jugador_hospi == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/jugador_familia/", response_model=schemas.JugadorFamiliaResponse, tags=["JugadorFamilia"])
def create_jugador_familia(item: schemas.JugadorFamiliaCreate, db: Session = Depends(get_db)):
    db_item = models.JugadorFamilia(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/jugador_familia/{item_id}", tags=["JugadorFamilia"])
def delete_jugador_familia(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.JugadorFamilia).filter(models.JugadorFamilia.id_jugador_hospi == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for EstadisticasJugador ---
@router.get("/estadisticas_jugador/", response_model=List[schemas.EstadisticasJugadorResponse], tags=["EstadisticasJugador"])
def read_estadisticas_jugador_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.EstadisticasJugador).offset(skip).limit(limit).all()

@router.get("/estadisticas_jugador/{item_id}", response_model=schemas.EstadisticasJugadorResponse, tags=["EstadisticasJugador"])
def read_estadisticas_jugador(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.EstadisticasJugador).filter(models.EstadisticasJugador.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/estadisticas_jugador/", response_model=schemas.EstadisticasJugadorResponse, tags=["EstadisticasJugador"])
def create_estadisticas_jugador(item: schemas.EstadisticasJugadorCreate, db: Session = Depends(get_db)):
    db_item = models.EstadisticasJugador(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/estadisticas_jugador/{item_id}", tags=["EstadisticasJugador"])
def delete_estadisticas_jugador(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.EstadisticasJugador).filter(models.EstadisticasJugador.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# --- CRUD for AnalisisPartido ---
@router.get("/analisis_partido/", response_model=List[schemas.AnalisisPartidoResponse], tags=["AnalisisPartido"])
def read_analisis_partido_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.AnalisisPartido).offset(skip).limit(limit).all()

@router.get("/analisis_partido/{item_id}", response_model=schemas.AnalisisPartidoResponse, tags=["AnalisisPartido"])
def read_analisis_partido(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.AnalisisPartido).filter(models.AnalisisPartido.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/analisis_partido/", response_model=schemas.AnalisisPartidoResponse, tags=["AnalisisPartido"])
def create_analisis_partido(item: schemas.AnalisisPartidoCreate, db: Session = Depends(get_db)):
    db_item = models.AnalisisPartido(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/analisis_partido/{item_id}", tags=["AnalisisPartido"])
def delete_analisis_partido(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.AnalisisPartido).filter(models.AnalisisPartido.id == item_id).first()
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}
