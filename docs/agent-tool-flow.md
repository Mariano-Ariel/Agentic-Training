# Agent Tool Flow — Arquitectura de Agentes con Tool Calling

## 1. Qué es Tool Calling

Tool calling es un mecanismo donde un LLM no ejecuta acciones directamente, sino que genera instrucciones estructuradas para que un sistema externo ejecute funciones determinísticas.

Esto permite combinar:
- razonamiento probabilístico (LLM)
- ejecución determinística (tools)

### Flujo conceptual

```txt
LLM (razonamiento)
→ interpretación de intención
→ decisión de uso de tools
→ emisión de llamada estructurada
→ Tool Runtime (ejecución externa)
→ resultado de la tool
→ LLM (síntesis final)
````

### Definición técnica

Tool calling = interfaz estructurada entre un modelo probabilístico y funciones externas ejecutables.

Ejemplo de llamada a tool:

```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "Mendoza"
  }
}
```

El LLM no ejecuta la función. Solo decide:

* cuándo usarla
* qué parámetros enviar

---

## 2. Cuándo usar Tools

Las tools se utilizan cuando la respuesta requiere información externa, dinámica o cálculo determinístico.

### Casos de uso

**Datos en tiempo real**

* clima
* hora actual
* cotizaciones
* stock o inventarios

**Integración con sistemas**

* APIs externas
* bases de datos
* microservicios

**Operaciones determinísticas**

* cálculos exactos
* transformaciones de datos
* validaciones

**Automatización**

* ejecución de workflows
* envío de requests
* triggers de procesos

---

### Cuándo NO usar tools

* conocimiento teórico o conceptual
* razonamiento interno del modelo
* respuestas basadas en entrenamiento
* consultas sin dependencia externa

---

## 3. Diferencia entre Prompt y Tool

Un sistema con LLM separa claramente lo que se responde con el modelo y lo que requiere ejecución externa.

### Prompt

Entrada textual procesada internamente por el LLM.

* no ejecuta acciones
* basado en conocimiento entrenado
* salida probabilística

Ejemplo:

> "Explicá cómo funciona la fotosíntesis"

---

### Tool

Función externa ejecutada por el sistema.

* ejecuta lógica real
* accede a datos dinámicos
* resultado determinístico
* independiente del modelo

Ejemplo:

> "Qué clima hace en Mendoza"

→ requiere `get_weather(city)`

---

### Comparación

| Característica | Prompt (LLM)   | Tool (Sistema externo) |
| -------------- | -------------- | ---------------------- |
| Ejecución      | Interna        | Externa                |
| Naturaleza     | Probabilística | Determinística         |
| Datos          | Estáticos      | Dinámicos              |
| Actualización  | No             | Sí                     |
| Control        | Modelo         | Sistema                |

---

## 4. Cómo decide un agente usar herramientas

Un agente implementa una capa de decisión que evalúa si debe responder directamente o usar tools.

### Flujo de decisión

```txt
Input usuario
→ análisis de intención
→ evaluación de necesidad externa
→ decisión (tool / no tool)
→ ejecución de tool (si aplica)
→ síntesis de respuesta
```

### Criterios de decisión

* ¿Requiere información en tiempo real?
* ¿Depende de un sistema externo?
* ¿Existe una herramienta más precisa que el LLM?
* ¿Se necesita un resultado determinístico?

Si alguna condición es verdadera → se usa tool.

---

### Ejemplo 1: sin tool

> "Qué es un embedding"

→ información interna suficiente
→ respuesta directa del LLM

---

### Ejemplo 2: con tool

> "Qué hora es en Japón"

```txt
intent: time
tool: get_time("Japan")
```

Output:

> "En Japón son las 14:32 actualmente."

---

## 5. Ejercicio práctico — Agente sin frameworks

### Objetivo

Diseñar un agente básico capaz de:

* consultar clima
* consultar hora
* responder preguntas generales

---

### Restricción

No usar frameworks externos (LangChain, CrewAI, AutoGPT, etc).

Solo lógica propia.

---

### Arquitectura mínima

El sistema se compone de tres módulos:

#### 1. Router de intención

Clasifica la entrada del usuario.

```txt
if "clima" in input → weather
if "hora" in input → time
else → general
```

Alternativa:

* LLM router que devuelve etiqueta: weather / time / general

---

#### 2. Tools disponibles

```txt
get_weather(city)
get_time(location)
```

---

#### 3. Flujo del agente

```txt
Usuario input
→ router de intención
→ selección de tool (si aplica)
→ ejecución de tool
→ si no aplica → LLM responde
→ output final
```

---

### Ejemplo de ejecución

#### Caso 1: clima

```txt
Input: "Qué clima hace en Mendoza?"

intent: weather
tool: get_weather("Mendoza")
resultado: 18°C soleado
```

Output:

> "En Mendoza actualmente hay 18°C y cielo despejado."

---

#### Caso 2: hora

```txt
Input: "Qué hora es en Japón?"

intent: time
tool: get_time("Japan")
resultado: 14:32 JST
```

Output:

> "En Japón son las 14:32 actualmente."

---

#### Caso 3: general

```txt
Input: "Qué es un agente en IA?"

intent: general
no tool
LLM responde directamente
```

---

## 6. Implementación práctica del sistema (AGENTIC-TRAINING)

La arquitectura teórica de tool calling fue implementada en un entorno funcional dentro del repositorio, separando la capa de documentación de la capa ejecutable.

El objetivo de esta separación es:

* desacople entre teoría y runtime
* modularidad del sistema
* escalabilidad hacia APIs o interfaces
* validación práctica del modelo de agente

---

## 6.1 Estructura del repositorio

```txt
AGENTIC-TRAINING/
│
├── docs/
│   ├── agent-tool-flow.md
│   ├── ai-agents.md
│   ├── embeddings-basics.md
│   ├── prompt-tests.md
│   └── methodology.md
│
├── practice/
│
│   ├── agent-runtime/
│   │   ├── agent.py
│   │   ├── tools.py
│   │   ├── router.py
│   │   └── config.py
│   │
│   ├── web_ui/
│   │   ├── backend.py
│   │   ├── frontend.html
│   │   └── static/
│   │
│   └── README.md
│
└── README.md
```

---

## 6.2 Mapeo teoría → implementación

### Router de intención

```txt
docs → decisión de tool
practice/agent-runtime/router.py
```

### Tools determinísticas

```txt
docs → get_weather / get_time
practice/agent-runtime/tools.py
```

### Orquestador del agente

```txt
docs → flujo LLM → router → tool → síntesis
practice/agent-runtime/agent.py
```

### Capa de ejecución externa

```txt
docs → Tool Runtime
practice/web_ui/backend.py
```

---

## 6.3 Flujo completo implementado

```txt
Frontend (HTML/JS)
        ↓
FastAPI backend (/chat)
        ↓
agent.py (orquestador)
        ↓
router.py (intención)
        ↓
tools.py (ejecución determinística)
        ↓
respuesta estructurada
        ↓
frontend render
```

---

## 6.4 Validación del modelo

El sistema implementado valida el concepto central de tool calling:

* el modelo no ejecuta acciones directamente
* la lógica se separa en capas independientes
* las tools son funciones determinísticas externas
* el flujo es auditable extremo a extremo

---

## 6.5 Resultado práctico

El agente implementado es capaz de:

* responder consultas generales
* consultar clima (mock o función local)
* consultar hora (mock o función local)
* exponer resultados vía API REST
* interactuar con interfaz web simple

---

## 6.6 Conclusión

Tool calling convierte un LLM en un sistema híbrido entre razonamiento y ejecución.

La arquitectura de agentes se basa en desacoplar:

* interpretación (LLM)
* decisión (router)
* ejecución (tools)
* síntesis (LLM)

Esto constituye la base funcional de sistemas de agentes modernos.
