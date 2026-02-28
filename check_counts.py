from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def check_counts():
    if not DATABASE_URL:
        print("DATABASE_URL not found")
        return

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    tables = ['eventos', 'partidos', 'entrenamientos', 'rivales', 'Staff', 'jugadores_propios', 'familias']
    
    print("\n--- Row counts in Neon DB ---")
    for table in tables:
        try:
            # Handle case sensitivity for "Staff"
            quoted_table = f'"{table}"' if any(c.isupper() for c in table) else table
            result = session.execute(text(f"SELECT COUNT(*) FROM {quoted_table}"))
            count = result.scalar()
            print(f"{table}: {count}")
        except Exception as e:
            print(f"{table}: Error - {e}")

    session.close()

if __name__ == "__main__":
    check_counts()
