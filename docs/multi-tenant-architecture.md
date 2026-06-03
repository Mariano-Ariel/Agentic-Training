# Guía Completa: Arquitectura Multi-Tenant para Plataformas SaaS Educativas

Esta guía consolida los conceptos fundamentales de arquitectura Multi-Tenant, aislamiento lógico, RBAC, gestión de tenants y escalabilidad, aplicados al diseño de plataformas educativas SaaS capaces de soportar múltiples instituciones utilizando infraestructura compartida.

---

# 1. Conceptos Fundamentales

Los sistemas SaaS multi-tenant permiten que múltiples clientes utilicen una misma aplicación sin compartir información sensible.

| Concepto                     | Definición Técnica                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------------------ |
| SaaS (Software as a Service) | Modelo donde una aplicación es consumida como servicio a través de internet.                     |
| Tenant                       | Cliente o entidad independiente dentro del sistema. En este caso, una escuela.                   |
| Multi-Tenant                 | Arquitectura donde múltiples tenants utilizan una misma aplicación e infraestructura compartida. |
| tenantId                     | Identificador único utilizado para separar datos y operaciones entre tenants.                    |
| JWT                          | Token de autenticación que transporta información del usuario y del tenant.                      |
| RBAC                         | Modelo de autorización basado en roles y permisos.                                               |
| RLS (Row Level Security)     | Mecanismo de base de datos que restringe el acceso a filas específicas según reglas definidas.   |

---

# 2. ¿Qué es una Arquitectura Multi-Tenant?

Una arquitectura multi-tenant permite que una única instancia de software atienda simultáneamente a múltiples clientes.

Ejemplo:

| Tenant   | Institución         |
| -------- | ------------------- |
| tenant_1 | Escuela San Martín  |
| tenant_2 | Escuela Belgrano    |
| tenant_3 | Escuela Técnica Nº5 |

Todos utilizan la misma aplicación.

Todos comparten la misma infraestructura.

Ninguno debe poder acceder a los datos de otro.

---

# 3. Ventajas y Desventajas

La adopción de una arquitectura multi-tenant presenta beneficios operativos importantes, pero también introduce desafíos de seguridad y diseño.

## Ventajas

| Ventaja                    | Descripción                                                 |
| -------------------------- | ----------------------------------------------------------- |
| Economía de escala         | Menor costo al compartir infraestructura.                   |
| Mantenimiento centralizado | Una actualización beneficia a todos los clientes.           |
| Escalabilidad              | Incorporar nuevos tenants requiere poco esfuerzo adicional. |
| Eficiencia operativa       | Mejor utilización de recursos computacionales.              |

## Desventajas

| Desventaja              | Descripción                                                     |
| ----------------------- | --------------------------------------------------------------- |
| Data Leaks              | Riesgo de exposición accidental entre tenants.                  |
| Noisy Neighbor          | Un tenant puede afectar el rendimiento de otros.                |
| Complejidad técnica     | Requiere controles de aislamiento y seguridad más sofisticados. |
| Mayor impacto de fallos | Una falla puede afectar a múltiples clientes simultáneamente.   |

---

# 4. Modelos de Separación de Tenants

Existen tres enfoques principales para almacenar información de múltiples escuelas.

| Modelo | Descripción                               | Ventajas                                 | Desventajas                       |
| ------ | ----------------------------------------- | ---------------------------------------- | --------------------------------- |
| Silo   | Una base de datos por escuela.            | Máximo aislamiento.                      | Costoso y difícil de administrar. |
| Bridge | Una base de datos con esquemas separados. | Buen equilibrio entre costo y seguridad. | Mayor complejidad operativa.      |
| Pool   | Base de datos compartida con tenantId.    | Escalable y económico.                   | Requiere controles estrictos.     |

Para una plataforma educativa SaaS moderna se recomienda inicialmente el modelo Pool.

---

# 5. Aislamiento Lógico

El aislamiento lógico consiste en separar información mediante reglas de software en lugar de infraestructura física independiente.

Ejemplo:

| id | tenantId  | alumno |
| -- | --------- | ------ |
| 1  | escuela_a | Juan   |
| 2  | escuela_a | María  |
| 3  | escuela_b | Pedro  |

Cuando una escuela realiza una consulta:

```sql
SELECT *
FROM alumnos
WHERE tenantId = 'escuela_a';
```

Solo obtiene sus propios registros.

---

# 6. RBAC (Role Based Access Control)

RBAC permite controlar qué acciones puede realizar cada usuario dentro de un tenant.

## Roles típicos

| Rol           | Permisos                            |
| ------------- | ----------------------------------- |
| Administrador | Gestión completa de la institución. |
| Profesor      | Gestión académica y carga de notas. |
| Estudiante    | Consulta de información personal.   |

Principio fundamental:

Un usuario solo puede acceder a recursos permitidos dentro de su tenant.

---

# 7. Gestión del tenantId

El tenantId constituye el principal mecanismo de separación de datos.

## Base de Datos

Debe existir como columna obligatoria en:

* alumnos
* docentes
* cursos
* materias
* pagos
* calificaciones

## JWT

Ejemplo:

```json
{
  "userId": 15,
  "tenantId": "escuela_a",
  "role": "profesor"
}
```

Cada petición transporta automáticamente el contexto del tenant.

---

# 8. Prevención de Filtraciones (Data Leaks)

El principal riesgo de una arquitectura multi-tenant es el acceso cruzado entre clientes.

## Técnicas recomendadas

### Validación de Tenant

Toda solicitud debe identificar y validar el tenant antes de ejecutar lógica de negocio.

### Row Level Security (RLS)

PostgreSQL puede aplicar filtros automáticos por tenantId.

Beneficio:

Reduce errores humanos en consultas SQL.

### Namespacing de Caché

Redis debe utilizar claves separadas.

Ejemplo:

```text
escuela_a:alumnos
escuela_b:alumnos
escuela_c:alumnos
```

### Auditoría

Registrar:

* usuario
* tenant
* acción realizada
* fecha y hora

---

# 9. Escalabilidad

La arquitectura debe evolucionar junto al crecimiento de la plataforma.

## Etapa 1: Hasta 100 Escuelas

* Monolito
* PostgreSQL
* Shared Database
* tenantId

## Etapa 2: Hasta 1.000 Escuelas

* Load Balancer
* Varias instancias de aplicación
* Caché Redis

## Etapa 3: Miles de Escuelas

* Sharding
* Caché distribuida
* Observabilidad centralizada
* Escalado horizontal

---

# 10. Arquitectura Recomendada

Flujo simplificado:

Frontend

↓

Autenticación

↓

JWT

↓

API

↓

RBAC

↓

Servicios

↓

PostgreSQL

↓

Redis

Todos los componentes utilizan tenantId como mecanismo principal de aislamiento.

---

# 11. Buenas Prácticas

### Seguridad

* Aplicar principio de mínimo privilegio.
* Utilizar RBAC en todas las operaciones.
* Validar tenant en cada request.

### Observabilidad

* Monitorear métricas por tenant.
* Mantener auditorías completas.

### Escalabilidad

* Diseñar para escalado horizontal.
* Evitar dependencias específicas por cliente.

### Mantenimiento

* Automatizar despliegues.
* Centralizar configuraciones.

---

# 12. Ideas Clave para Recordar

* Multi-Tenant significa múltiples clientes en una misma aplicación.
* Tenant es el cliente aislado dentro del sistema.
* tenantId es la frontera principal de seguridad.
* RBAC controla qué puede hacer cada usuario.
* RLS protege contra errores humanos.
* El principal riesgo es el Data Leak.
* Pool Model suele ser la mejor opción para SaaS de alta escala.
* Escalabilidad y aislamiento deben diseñarse desde el inicio.
* Toda arquitectura SaaS moderna gira alrededor de identidad, autorización y aislamiento de datos.
