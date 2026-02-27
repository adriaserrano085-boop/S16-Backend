import os
import uuid
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from datetime import datetime

# Import models to ensure they are registered and can be used for insertion
import models_auto as models

load_dotenv()

OLD_DB_URL = os.getenv("OLD_DATABASE_URL")
NEW_DB_URL = os.getenv("DATABASE_URL")

def migrate_table(old_db, new_db, model_class):
    table_name = model_class.__tablename__
    print(f"📦 Migrando tabla: {table_name}...")
    
    # Get all rows from old table
    try:
        # We use public schema explicitly if needed, but usually default is public
        # Using double quotes for tables that might be case sensitive or reserved words like "Staff"
        quoted_table = f'"{table_name}"' if any(c.isupper() for c in table_name) else table_name
        result = old_db.execute(text(f"SELECT * FROM public.{quoted_table}"))
        rows = result.fetchall()
        columns = result.keys()
        
        count = 0
        for row in rows:
            # Map row to dictionary
            row_dict = dict(zip(columns, row))
            
            # Create model instance
            # We filter only keys that exist in the model to avoid errors
            filtered_dict = {k: v for k, v in row_dict.items() if hasattr(model_class, k)}
            
            # Handle timestamps/dates if they are strings in old DB but objects in new (SQLAlchemy usually handles this)
            
            db_item = model_class(**filtered_dict)
            
            try:
                # Merge or add? If we want to avoid duplicates and we have PKs
                new_db.merge(db_item)
                count += 1
            except Exception as e:
                print(f"  ⚠️ Error insertando fila en {table_name}: {e}")
                new_db.rollback()
        
        new_db.commit()
        print(f"✅ Migrados {count} registros en {table_name}.")
    except Exception as e:
        print(f"❌ Error migrando {table_name}: {e}")
        new_db.rollback()

def main():
    if not OLD_DB_URL or not NEW_DB_URL:
        print("❌ Error: Faltan URLs de base de datos en .env")
        return

    old_engine = create_engine(OLD_DB_URL)
    new_engine = create_engine(NEW_DB_URL)
    
    OldSession = sessionmaker(bind=old_engine)
    NewSession = sessionmaker(bind=new_engine)
    
    old_db = OldSession()
    new_db = NewSession()
    
    # List of tables to migrate in order of dependency if possible
    # (Simplified: independent first or just try-catch)
    tables = [
        models.Rivales,
        models.Eventos,
        models.Entrenamientos,
        models.Partidos,
        models.PartidosExternos,
        models.JugadoresPropios,
        models.Staff,
        models.Familias,
        models.Asistencia,
        models.EstadisticasPartido,
        models.EstadisticasJugador,
        models.Convocatoria,
        models.JugadorFamilia,
        models.AnalisisPartido,
        models.JugadoresExternos
    ]
    
    print("🚀 Iniciando volcado total de datos...")
    for model in tables:
        migrate_table(old_db, new_db, model)
    
    print("\n✨ Proceso de migración completado.")
    old_db.close()
    new_db.close()

if __name__ == "__main__":
    main()
