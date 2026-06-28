# Async AI Processing

## Objetivo

Diseñar una arquitectura escalable para sistemas de Inteligencia Artificial que permita ejecutar tareas de larga duración sin bloquear la aplicación principal.

Este documento estudia los fundamentos del procesamiento asíncrono, el uso de colas de trabajo, workers y sistemas de background processing, para posteriormente aplicarlos a un pipeline de análisis documental basado en IA.

---

# 1. El problema de los procesos síncronos

La mayoría de las aplicaciones web tradicionales utilizan un modelo **Request → Response**.

```text
Cliente
    ↓
Servidor
    ↓
Procesamiento
    ↓
Respuesta
```

Este modelo funciona correctamente cuando el tiempo de procesamiento es corto.

Ejemplos:

* autenticación
* consultas SQL
* operaciones CRUD
* búsquedas simples
* actualizaciones de registros

Sin embargo, los sistemas de IA presentan una característica diferente:

* OCR
* procesamiento de PDFs
* embeddings
* retrieval
* llamadas a LLM
* clasificación documental
* análisis multimodal

Estas tareas pueden requerir:

* segundos
* decenas de segundos
* minutos
* procesamiento distribuido

---

## Problemas del procesamiento síncrono

Cuando una tarea de IA se ejecuta dentro del request principal aparecen problemas como:

### Timeouts

```text
Cliente
    ↓
Servidor
    ↓
IA (45 segundos)
    ↓
Timeout
```

---

### Bloqueo de recursos

Mientras el procesamiento continúa:

* conexiones quedan abiertas
* memoria permanece reservada
* threads quedan ocupados
* disminuye la capacidad del sistema

---

### Mala experiencia de usuario

El usuario debe esperar hasta que finalice el procesamiento.

---

### Baja escalabilidad

Un servidor solo puede ejecutar una cantidad limitada de tareas simultáneas.

---

# 2. Procesamiento Asíncrono

El procesamiento asíncrono consiste en separar:

* recepción del trabajo
* ejecución del trabajo

En lugar de:

```text
Cliente
    ↓
Procesar
    ↓
Esperar
    ↓
Responder
```

se realiza:

```text
Cliente
    ↓
Registrar trabajo
    ↓
Responder
    ↓
Procesar posteriormente
```

El usuario recibe una respuesta inmediata mientras el trabajo continúa en segundo plano.

---

## Ventajas

* menor latencia percibida
* mejor experiencia de usuario
* desacoplamiento
* mayor capacidad de procesamiento
* tolerancia a fallos
* escalabilidad horizontal

---

# 3. Queues

Una Queue (cola) es una estructura utilizada para almacenar tareas pendientes de ejecución.

Su función principal es desacoplar:

* productores
* consumidores

```text
Producer
     ↓
   Queue
     ↓
Consumer
```

---

## Analogía

Un restaurante:

```text
Cliente
    ↓
Mozo
    ↓
Comanda
    ↓
Cocina
```

El cliente no cocina la comida.

La cocina trabaja independientemente.

---

## Beneficios

* desacoplamiento
* control de carga
* balanceo
* reintentos
* procesamiento diferido
* escalabilidad

---

# 4. Jobs

Un Job representa una unidad individual de trabajo.

Ejemplo:

```json
{
    "id": "job_145",
    "userId": "user_12",
    "documentId": "pdf_456",
    "type": "document-analysis"
}
```

---

## Información típica

Un job contiene:

* identificador
* payload
* prioridad
* estado
* timestamps
* errores
* resultado

---

## Estados

```text
waiting
active
completed
failed
delayed
paused
```

---

## Ciclo de vida

```text
Created
    ↓
Queued
    ↓
Processing
    ↓
Completed
```

o

```text
Created
    ↓
Queued
    ↓
Processing
    ↓
Failed
```

---

# 5. Workers

Un Worker es un proceso independiente encargado de ejecutar jobs.

```text
Queue
   ↓
Worker
   ↓
Execute
```

---

## Responsabilidades

Un worker puede:

* consumir jobs
* ejecutar lógica
* llamar APIs
* utilizar LLMs
* guardar resultados
* manejar errores
* reintentar procesos

---

## Escalado horizontal

```text
Queue
   ↓
Worker 1
Worker 2
Worker 3
Worker N
```

Cuantos más workers existan, mayor capacidad tendrá el sistema.

---

# 6. Background Jobs

Los background jobs son tareas ejecutadas fuera del request principal.

Ejemplos:

* envío de emails
* generación de PDFs
* creación de thumbnails
* procesamiento de video
* análisis mediante IA

---

## Flujo

```text
Request
    ↓
Crear Job
    ↓
Respuesta inmediata
    ↓
Background Processing
```

---

# 7. Message Brokers

Un Message Broker es un sistema encargado de transportar mensajes entre procesos desacoplados.

Su objetivo es permitir que:

* productores
* consumidores

trabajen independientemente.

---

## Ejemplos

| Tecnología | Uso principal         |
| ---------- | --------------------- |
| Redis      | Colas rápidas         |
| RabbitMQ   | Mensajería robusta    |
| Kafka      | Eventos masivos       |
| NATS       | Sistemas distribuidos |

---

# 8. Redis como sistema de colas

Redis es una base de datos en memoria extremadamente rápida.

Puede utilizarse como:

* cache
* message broker
* queue engine
* almacenamiento temporal

---

## Ventajas

* baja latencia
* alta concurrencia
* persistencia opcional
* escalabilidad
* simplicidad operativa

---

## Flujo

```text
API
   ↓
Redis Queue
   ↓
Worker
```

---

# 9. BullMQ

BullMQ es una librería para Node.js que implementa un sistema completo de procesamiento de jobs utilizando Redis.

---

## Componentes

```text
Queue
Job
Worker
QueueEvents
FlowProducer
```

---

## Funcionalidades

BullMQ proporciona:

* retries
* delayed jobs
* priorities
* concurrency
* rate limiting
* monitoring
* event listeners
* distributed workers

---

## Arquitectura básica

```text
API
   ↓
BullMQ Queue
   ↓
Redis
   ↓
BullMQ Worker
```

---

# 10. Escalabilidad Horizontal

Una arquitectura síncrona:

```text
API
 ↓
LLM
```

posee un límite físico.

---

Una arquitectura basada en workers permite:

```text
Queue
  ↓
W1
W2
W3
W4
WN
```

Incrementando workers aumenta la capacidad total.

---

## Beneficios

* paralelismo
* elasticidad
* alta disponibilidad
* distribución de carga
* resiliencia

---

# 11. Arquitecturas Event Driven

Las arquitecturas modernas se basan en eventos.

```text
Evento
    ↓
Queue
    ↓
Worker
    ↓
Nuevo Evento
```

---

## Beneficios

* desacoplamiento
* tolerancia a fallos
* observabilidad
* escalabilidad
* extensibilidad

---

# 12. Aplicación a sistemas IA

## Problema

El procesamiento documental mediante IA puede tardar varios minutos.

Ejemplo:

```text
PDF
 ↓
OCR
 ↓
Chunking
 ↓
Embeddings
 ↓
Retrieval
 ↓
LLM
 ↓
Clasificación
```

Ejecutar este flujo dentro del request HTTP resulta ineficiente.

---

# 13. Arquitectura propuesta

La solución consiste en desacoplar completamente el procesamiento.

```text
Usuario
    │
    │ Upload PDF
    ▼
API Server
    │
    │ Crear Job
    ▼
BullMQ Queue
    │
    ▼
Redis
    │
    ▼
AI Worker
    │
    ├── OCR
    ├── Chunking
    ├── Embeddings
    ├── Retrieval
    ├── LLM Analysis
    └── Classification
    │
    ▼
Database
    │
    ▼
Result API
```

---

# 14. Flujo completo

## Paso 1

El usuario sube un PDF.

```http
POST /documents
```

---

## Paso 2

La API:

* almacena el archivo
* crea un job
* devuelve inmediatamente un identificador

```json
{
    "jobId": "job_845",
    "status": "queued"
}
```

---

## Paso 3

BullMQ almacena el trabajo.

```text
Job
    ↓
Redis Queue
```

---

## Paso 4

Un AI Worker consume el trabajo.

```text
Redis
    ↓
Worker
```

---

## Paso 5

El worker ejecuta:

```text
OCR
 ↓
Chunking
 ↓
Embeddings
 ↓
Retrieval
 ↓
LLM
 ↓
Classification
```

---

## Paso 6

El resultado es persistido.

```text
Worker
   ↓
Database
```

---

## Paso 7

El usuario consulta el estado.

```http
GET /jobs/job_845
```

Respuesta:

```json
{
    "status": "completed",
    "result": {}
}
```

---

# 15. Arquitectura objetivo

```text
PDF Upload
      ↓
API
      ↓
BullMQ Queue
      ↓
Redis
      ↓
AI Workers
      ↓
LLM Processing
      ↓
Database
      ↓
Result API
```

---

# 16. Evolución hacia Agentic AI

La arquitectura basada en queues es el paso previo natural a sistemas agentic.

Arquitectura actual:

```text
Request
    ↓
Queue
    ↓
Worker
    ↓
LLM
    ↓
Result
```

Arquitectura Agentic:

```text
Event
   ↓
Queue
   ↓
Agent Worker
   ↓
Planner
   ↓
Tools
   ↓
Memory
   ↓
Event Bus
   ↓
Next Agent
```

Los sistemas multiagente modernos son, esencialmente, sistemas distribuidos construidos sobre procesamiento asíncrono, eventos y colas de trabajo.
