import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# We will use Neon.tech or a local postgres database.
# Ensure you set DATABASE_URL in your .env file
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    print("WARNING: DATABASE_URL not found in environment variables. Falling back to localhost.")
    SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
else:
    print(f"DATABASE_URL found. Protocol: {SQLALCHEMY_DATABASE_URL.split(':')[0]}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
