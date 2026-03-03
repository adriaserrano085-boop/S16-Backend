import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os

DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_8qBxyj5dFpAL@ep-cool-butterfly-a2b1yqf3-pooler.eu-central-1.aws.neon.tech/neondb?ssl=require"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def main():
    async with AsyncSessionLocal() as session:
        query = text("""
            UPDATE "PruebasFisicas" p
            SET broncotest_20m = p.broncotest, broncotest = NULL
            FROM jugadores_propios j
            WHERE p.jugador_id = j.id
            AND p.fecha = '2025-11-01'
            AND p.broncotest IS NOT NULL
            AND (
                j.nombre ILIKE '%Adrian%' OR 
                j.nombre ILIKE '%Alex%' OR 
                j.nombre ILIKE '%Alexis%' OR 
                j.nombre ILIKE '%Xavi%' OR 
                j.nombre ILIKE '%Victor%'
            )
        """)
        
        result = await session.execute(query)
        await session.commit()
        print(f"Updated {result.rowcount} rows.")

if __name__ == "__main__":
    asyncio.run(main())
