import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def main():
    if not DB_URL:
        print("❌ Error: DATABASE_URL not found in .env")
        return

    print(f"🔌 Connecting to {DB_URL.split('@')[-1]}...")
    engine = create_engine(DB_URL)
    
    columns_to_add = [
        ("posesion_local", "INTEGER"),
        ("posesion_visitante", "INTEGER"),
        ("placajes_hechos_local", "INTEGER"),
        ("placajes_hechos_visitante", "INTEGER"),
        ("placajes_fallados_local", "INTEGER"),
        ("placajes_fallados_visitante", "INTEGER"),
        ("mele_ganada_local", "INTEGER"),
        ("mele_ganada_visitante", "INTEGER"),
        ("mele_perdida_local", "INTEGER"),
        ("mele_perdida_visitante", "INTEGER"),
        ("touch_ganada_local", "INTEGER"),
        ("touch_ganada_visitante", "INTEGER"),
        ("touch_perdida_local", "INTEGER"),
        ("touch_perdida_visitante", "INTEGER"),
    ]

    with engine.connect() as conn:
        for col_name, col_type in columns_to_add:
            try:
                print(f"Adding column {col_name}...")
                conn.execute(text(f"ALTER TABLE estadisticas_partido ADD COLUMN {col_name} {col_type}"))
                conn.commit()
                print(f"✅ Column {col_name} added.")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print(f"ℹ️ Column {col_name} already exists.")
                else:
                    print(f"❌ Error adding column {col_name}: {e}")

    print("🚀 All columns processed!")

if __name__ == "__main__":
    main()
