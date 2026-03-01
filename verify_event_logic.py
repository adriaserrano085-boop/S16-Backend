import sys
import os
from datetime import date, time
from sqlalchemy.orm import Session

# Add current directory to path
sys.path.append(os.getcwd())

import models_auto as models
import schemas_auto as schemas
from database import SessionLocal

def verify():
    db: Session = SessionLocal()
    try:
        test_fecha = date(2025, 12, 25)
        test_hora = time(10, 0)
        
        # 1. Clean up potential previous test data
        existing = db.query(models.Eventos).filter(
            models.Eventos.fecha == test_fecha,
            models.Eventos.hora == test_hora
        ).first()
        if existing:
            # Delete children first
            db.query(models.Entrenamientos).filter(models.Entrenamientos.evento == existing.id).delete()
            db.query(models.Partidos).filter(models.Partidos.Evento == existing.id).delete()
            db.query(models.Eventos).filter(models.Eventos.id == existing.id).delete()
            db.commit()

        # 2. Test create via logic (simulating the router logic)
        print("Testing Training Creation...")
        from routers_auto import crear_o_actualizar_evento
        
        training_data = schemas.EventoCreateUpdate(
            tipo="Entrenamiento",
            fecha=test_fecha,
            hora=test_hora,
            calentamiento="Test Warmup"
        )
        
        ev1 = crear_o_actualizar_evento(training_data, db)
        print(f"Created Event ID: {ev1.id}")
        
        # Verify training exists
        t = db.query(models.Entrenamientos).filter(models.Entrenamientos.evento == ev1.id).first()
        assert t is not None, "Training was not created"
        assert t.calentamiento == "Test Warmup"
        print("Training creation verified.")

        # 3. Test upsert (same date/time)
        print("Testing Upsert (Update existing by date/time)...")
        update_data = schemas.EventoCreateUpdate(
            tipo="Entrenamiento",
            fecha=test_fecha,
            hora=test_hora,
            calentamiento="Updated Warmup"
        )
        
        ev2 = crear_o_actualizar_evento(update_data, db)
        print(f"Upserted Event ID: {ev2.id}")
        
        assert ev1.id == ev2.id, "Upsert created a new event instead of updating"
        
        t_updated = db.query(models.Entrenamientos).filter(models.Entrenamientos.evento == ev2.id).first()
        assert t_updated.calentamiento == "Updated Warmup", "Training details were not updated"
        print("Upsert verified successfully.")

        # 4. Test Match creation/update naming fix
        print("Testing Match Creation...")
        match_fecha = date(2025, 12, 26)
        match_data = schemas.EventoCreateUpdate(
            tipo="Partido",
            fecha=match_fecha,
            hora=test_hora,
            lugar="Test Stadium"
        )
        
        ev_m = crear_o_actualizar_evento(match_data, db)
        print(f"Created Match Event ID: {ev_m.id}")
        
        m = db.query(models.Partidos).filter(models.Partidos.Evento == ev_m.id).first()
        assert m is not None, "Match was not created (check attribute naming)"
        assert m.lugar == "Test Stadium"
        print("Match creation/naming verified.")

        print("\nALL VERIFICATIONS PASSED!")

    except Exception as e:
        print(f"\nVERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    verify()
