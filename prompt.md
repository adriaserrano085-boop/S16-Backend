Rol: Arquitecto de Software Senior con enfoque en Seguridad (RBAC).

Misión: Desarrollar un backend en FastAPI para migrar una app de rugby desde Supabase a un sistema independiente y escalable.

1. Lógica de Gestión de Usuarios (Requisito Crítico):
Implementa una función de validación para la creación/actualización de usuarios con las siguientes reglas:

Solo el rol 'ADMIN' puede crear o asignar los roles 'ADMIN' y 'STAFF'.

El rol 'STAFF' puede crear usuarios y asignar los roles 'JUGADOR' y 'FAMILIA', además de vincularlos entre sí.

Si un 'STAFF' intenta asignar un rol de nivel superior, el sistema debe devolver un error 403 Forbidden.

2. Modelado de Datos para Migración:

Recrea la estructura de tablas de Supabase en SQLAlchemy para PostgreSQL.

Añade la tabla UserRoles y una tabla de unión FamilyPlayers para gestionar la relación de padres e hijos.

Incluye el módulo de Estadísticas Integrales: Melés (ganadas/perdidas/robadas), Touches, Placajes, Disciplina y Anotaciones.

3. Endpoints de Administración:

POST /users/assign-role: Endpoint protegido que valide quién está haciendo la petición y qué rol intenta asignar.

GET /users/pending: Lista de nuevos registros (familias/jugadores) que el Staff debe validar.

4. Infraestructura:

Configura CORS para el frontend en Vercel.

Prepara el Dockerfile para despliegue en Render y la conexión a Neon.tech.

Acción inicial: Genera el modelo de usuarios y el decorador de Python o la dependencia de FastAPI que verifique estos permisos de jerarquía antes de ejecutar cualquier cambio en la base de datos.
