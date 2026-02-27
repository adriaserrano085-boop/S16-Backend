# Catálogo de API - S16 Rugby App

Esta API está diseñada para centralizar la gestión de usuarios, roles, estadísticas y eventos del club.

**Base URL (Railway):** `https://s16-backend-production.up.railway.app` (Verificar URL real en panel)
**Documentación Interactiva:** `/docs` (Swagger UI)

## 1. Autenticación (JWT)

El sistema utiliza Bearer Tokens para la seguridad.

### Iniciar Sesión (Login)
- **Endpoint:** `POST /token`
- **Formato:** `x-www-form-urlencoded`
- **Campos:** `username` (email), `password`
- **Respuesta:** `{ "access_token": "...", "token_type": "bearer" }`

---

## 2. Gestión de Usuarios y Roles

### Asignar Nuevo Rol
- **Endpoint:** `POST /users/assign-role`
- **Header:** `Authorization: Bearer <token>`
- **Body (JSON):**
  ```json
  {
    "target_user_id": 12,
    "new_role": "STAFF"
  }
  ```

### Ver Registros Pendientes
- **Endpoint:** `GET /users/pending`
- **Descripción:** Devuelve los usuarios Jugador/Familia que aún no han sido validados por Staff.

### Vincular Padre a Hijo
- **Endpoint:** `POST /users/link-family`
- **Body (JSON):**
  ```json
  {
    "family_user_id": 1,
    "player_user_id": 5
  }
  ```

---

## 3. Endpoints CRUD Automáticos (v1)

Todas las tablas migradas tienen 4 métodos estándar bajo el prefijo `/api/v1/`.

| Tabla | Endpoint Base | Descripción |
| :--- | :--- | :--- |
| **Asistencia** | `/api/v1/asistencia/` | Control de asistencia a entrenamientos |
| **Entrenamientos** | `/api/v1/entrenamientos/` | Listado y detalles de sesiones |
| **Partidos** | `/api/v1/partidos/` | Información de encuentros RC Hospitalet |
| **Eventos** | `/api/v1/eventos/` | Calendario general |
| **Estadísticas Jugador** | `/api/v1/estadisticas_jugador/` | Números individuales por partido |
| **Convocatoria** | `/api/v1/convocatoria/` | Listas de jugadores por encuentro |
| **Rivales** | `/api/v1/rivales/` | Clubes opuestos y sus escudos |
| **Jugadores Propios** | `/api/v1/jugadores_propios/` | Fichas técnicas de los jugadores |
| **Familias** | `/api/v1/familias/` | Información de contacto de tutores |
| **Análisis Partido** | `/api/v1/analisis_partido/` | Reportes técnicos post-partido |

### Métodos Estándar por Tabla:
1. `GET /api/v1/<tabla>/` - Lista registros (paginado con `skip` y `limit`).
2. `GET /api/v1/<tabla>/{id}` - Detalles de un registro específico.
3. `POST /api/v1/<tabla>/` - Crear nuevo registro (requiere JSON).
4. `DELETE /api/v1/<tabla>/{id}` - Eliminar registro.

---

## 4. Estructura de Roles y Permisos (RBAC)

1. **ADMIN**: Control total. Puede asignar cualquier rol.
2. **STAFF**: Gestión operativa. Puede validar jugadores/familias y vincularlos. No puede crear otros Staff o Admins.
3. **JUGADOR / FAMILIA**: Acceso de consulta a sus propios datos y calendario.
