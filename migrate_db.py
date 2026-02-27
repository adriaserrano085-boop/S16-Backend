import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from passlib.context import CryptContext

import models

load_dotenv()

OLD_DB_URL = os.getenv("OLD_DATABASE_URL")
NEW_DB_URL = os.getenv("DATABASE_URL")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def main():
    if not OLD_DB_URL or not NEW_DB_URL:
        print("❌ Error: Faltan las variables DATABASE_URL o OLD_DATABASE_URL en .env")
        return

    if OLD_DB_URL == NEW_DB_URL:
        print("⚠️ Advertencia: OLD_DATABASE_URL y DATABASE_URL son iguales.")
        print("Por favor, asegúrate de poner la URL de conexión de Supabase en OLD_DATABASE_URL.")
        return

    print("🔌 Conectando a bases de datos...")
    try:
        old_engine = create_engine(OLD_DB_URL)
        new_engine = create_engine(NEW_DB_URL)
        
        # Asegurarnos de que las tablas en Neon existen
        models.Base.metadata.create_all(bind=new_engine)

        OldSession = sessionmaker(bind=old_engine)
        NewSession = sessionmaker(bind=new_engine)
        
        old_db = OldSession()
        new_db = NewSession()
        
        print("🚀 Iniciando migración de datos...")
        
        """
        NOTA PARA EL USUARIO:
        Dependiendo de cómo estuvieran tus datos en Supabase, tendrás que adaptar esta consulta.
        Supabase usa 'auth.users' para los correos, y quizás tenías una tabla 'profiles' en public.
        Este es un ejemplo genérico asumiendo que tenías una tabla llamada 'usuarios_antiguos' 
        o algo equivalente. Se recomienda usar text() para consultas SQL crudas en la BD antigua.
        """
        
        # 1. Obtener todos los IDs y correos de auth.users
        users_result = old_db.execute(text("SELECT id, email FROM auth.users")).fetchall()
        
        # 2. Mapas de roles
        staff_ids = set([r[0] for r in old_db.execute(text("SELECT auth_id FROM public.\"Staff\" WHERE auth_id IS NOT NULL")).fetchall()])
        familia_ids = set([r[0] for r in old_db.execute(text("SELECT id_usuario FROM public.familias WHERE id_usuario IS NOT NULL")).fetchall()])
        jugador_ids = set([r[0] for r in old_db.execute(text("SELECT \"Usuario\" FROM public.jugadores_propios WHERE \"Usuario\" IS NOT NULL")).fetchall()])

        admin_emails = ["adriserrajime@gmail.com"] # Aseguramos que tú seas ADMIN

        for row in users_result:
            u_id = row[0]
            email = row[1]
            
            # Determinar Rol
            role = models.RoleEnum.JUGADOR # Por defecto
            if str(u_id) in staff_ids:
                role = models.RoleEnum.STAFF
            elif str(u_id) in familia_ids:
                role = models.RoleEnum.FAMILIA
            elif str(u_id) in jugador_ids:
                role = models.RoleEnum.JUGADOR
                
            # Sobrescribir con ADMIN si el usuario es el dueño
            if email and email.lower() in admin_emails:
                role = models.RoleEnum.ADMIN
                
            if email:
                # Crear usuario en Neon
                new_user = models.User(
                    email=email,
                    hashed_password=pwd_context.hash("S16Rugby2026!"), # Contraseña temporal fija
                    role=role,
                    is_active=True,
                    is_pending_validation=False
                )
                new_db.add(new_user)
        
        # Guardar en Neon
        new_db.commit()
        
        print("✅ Migración (plantilla) finalizada.")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {str(e)}")
    finally:
        old_db.close()
        new_db.close()

if __name__ == "__main__":
    main()
