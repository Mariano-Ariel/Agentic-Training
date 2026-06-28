# Security Basics

## Objetivo

Comprender los principios fundamentales de seguridad necesarios para desplegar aplicaciones en producción y entender por qué la seguridad es un requisito arquitectónico y no una característica opcional.

Este documento estudia los riesgos más comunes en aplicaciones web modernas, APIs y sistemas basados en IA.

---

# 1. ¿Por qué producción da miedo?

Durante el desarrollo trabajamos en un entorno controlado:

* datos de prueba
* pocos usuarios
* acceso local
* infraestructura conocida

En producción ocurre lo contrario:

* usuarios desconocidos
* bots automatizados
* escáneres de vulnerabilidades
* ataques oportunistas
* errores humanos
* fallos de configuración

La pregunta deja de ser:

> "¿Me van a atacar?"

y pasa a ser:

> "¿Cuándo y cómo me van a atacar?"

---

# 2. Pensamiento de seguridad

La seguridad consiste en responder cuatro preguntas:

| Pregunta               | Objetivo   |
| ---------------------- | ---------- |
| ¿Qué protejo?          | Activos    |
| ¿Quién puede atacarlo? | Amenazas   |
| ¿Qué pasa si falla?    | Impacto    |
| ¿Cómo reduzco el daño? | Mitigación |

---

# 3. Autenticación y autorización

## Autenticación

Responde:

> ¿Quién eres?

```text
Usuario
   ↓
Credenciales
   ↓
Verificación
   ↓
Identidad
```

---

## Autorización

Responde:

> ¿Qué puedes hacer?

```text
Usuario autenticado
        ↓
Verificar permisos
        ↓
Acceso permitido
```

---

# 4. JWT (JSON Web Tokens)

JWT es un mecanismo de autenticación basado en tokens firmados.

Estructura:

```text
HEADER
   .
PAYLOAD
   .
SIGNATURE
```

---

## Flujo

```text
Login
   ↓
Servidor
   ↓
JWT
   ↓
Cliente
   ↓
Requests autenticados
```

---

## Activo protegido

* identidad del usuario
* sesiones
* permisos

---

## Amenaza

Exposición del secreto de firmado.

---

## ¿Qué pasa si exponemos JWT_SECRET?

Si un atacante obtiene el secreto:

```text
Atacante
     ↓
Obtiene JWT_SECRET
     ↓
Genera token falso
     ↓
Se convierte en administrador
```

Consecuencias:

* robo total de sesiones
* escalamiento de privilegios
* acceso a datos privados
* compromiso completo del sistema

---

## Mitigaciones

* variables de entorno
* rotación de secretos
* gestores de secretos
* expiración corta de tokens

---

# 5. CORS

CORS define qué dominios pueden utilizar nuestra API desde un navegador.

---

## Configuración segura

```text
frontend.miapp.com
        ↓
API
```

---

## Configuración insegura

```javascript
origin: "*"
```

---

## Activo protegido

* acceso a la API
* datos del usuario
* recursos del backend

---

## ¿Qué pasa si dejamos CORS abierto?

```text
Sitio malicioso
       ↓
Javascript
       ↓
Nuestra API
```

Consecuencias:

* abuso de endpoints
* scraping
* automatización de ataques
* exposición indirecta de información

---

## Mitigaciones

* whitelist de dominios
* separación dev/prod
* evitar "*"

---

# 6. Rate Limiting

Rate limiting controla cuántas solicitudes puede realizar un cliente.

---

## Problema

```text
Bot
 ↓
100000 requests
 ↓
Servidor saturado
```

---

## Solución

```text
Bot
 ↓
100 requests
 ↓
Bloqueado
```

---

## Activo protegido

* CPU
* memoria
* APIs
* presupuesto

---

## Mitigaciones

* límites por IP
* límites por usuario
* límites por API key
* throttling

---

# 7. Uploads

Los uploads constituyen una de las superficies de ataque más grandes.

---

## Riesgos

* malware
* payloads maliciosos
* archivos gigantes
* archivos corruptos
* ataques a parsers

---

## ¿Qué pasa si aceptamos cualquier PDF?

### Denial of Service

```text
PDF gigante
     ↓
Memoria agotada
```

---

### Parser Exploit

```text
PDF malicioso
      ↓
Parser vulnerable
      ↓
Compromiso del sistema
```

---

### Cost Explosion

```text
PDF enorme
      ↓
OCR
      ↓
Embeddings
      ↓
LLM
      ↓
Costos descontrolados
```

---

## Mitigaciones

Validar:

* extensión
* MIME type
* tamaño
* cantidad de páginas
* estructura
* antivirus

---

# 8. Secrets

Los secretos permiten acceder a recursos críticos.

Ejemplos:

* JWT_SECRET
* DATABASE_PASSWORD
* OPENAI_API_KEY
* AWS_SECRET_KEY

---

## Mala práctica

```javascript
const SECRET = "123456";
```

---

## Buena práctica

```javascript
process.env.JWT_SECRET
```

---

## Reglas

* nunca subir secretos a Git
* usar variables de entorno
* rotar credenciales
* aplicar mínimo privilegio

---

# 9. OWASP Basics

OWASP identifica los riesgos más comunes en aplicaciones.

---

## Broken Authentication

Fallas en login y sesiones.

---

## Broken Access Control

Acceso a recursos no autorizados.

---

## Cryptographic Failures

Uso incorrecto de secretos y cifrado.

---

## Injection

Entrada maliciosa ejecuta código.

Ejemplos:

* SQL Injection
* Command Injection
* Prompt Injection

---

## Security Misconfiguration

Configuraciones inseguras.

Ejemplos:

* CORS abierto
* debug habilitado
* credenciales por defecto

---

# 10. Seguridad en sistemas IA

Los sistemas de IA introducen nuevos vectores de ataque:

* prompt injection
* document poisoning
* token abuse
* cost explosion
* model abuse

---

# 11. Respuestas rápidas

## ¿Qué pasa si exponemos JWT_SECRET?

El atacante puede generar tokens válidos y comprometer completamente la autenticación.

---

## ¿Qué pasa si dejamos CORS abierto?

Cualquier sitio puede interactuar con nuestra API y facilitar ataques automatizados.

---

## ¿Qué pasa si aceptamos cualquier PDF?

Podemos sufrir:

* denegación de servicio
* explotación de parsers
* costos elevados
* procesamiento malicioso

---

# Conclusión

La seguridad no consiste en construir sistemas imposibles de atacar.

Consiste en asumir que el ataque ocurrirá y diseñar la arquitectura para:

* reducir la superficie de ataque
* limitar privilegios
* minimizar daños
* detectar incidentes
* recuperarse rápidamente

```
```
