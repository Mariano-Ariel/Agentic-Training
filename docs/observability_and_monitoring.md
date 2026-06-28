# Monitoring and Observability en Sistemas SaaS

## Objetivo de la solución
Diseñar un modelo operativo para detectar cuándo una **escuela (tenant)** está teniendo problemas en producción, usando señales técnicas del sistema.
La detección no depende de una única fuente, sino de la **correlación de logs, métricas y tracing**, segmentados por `schoolId`.

---

# 1. Base conceptual: Observabilidad

## Qué es
Observabilidad es la capacidad de entender el estado interno de un sistema a partir de sus salidas externas.

## Por qué existe
En sistemas SaaS modernos no es viable inspeccionar servidores directamente. En su lugar, se trabaja con señales indirectas:

- Logs → eventos
- Métricas → comportamiento agregado
- Tracing → flujo de ejecución

## Por qué es clave en esta solución
Porque permite responder una pregunta crítica:

> “¿Qué le está pasando a una escuela específica sin entrar al sistema manualmente?”

---

# 2. Logs (señales puntuales)

## Qué son
Eventos discretos que ocurren dentro del sistema en tiempo real.

## Qué aportan
- Información exacta de errores
- Contexto por request (`schoolId`, `requestId`)
- Evidencia concreta de fallos

## Por qué se usan en la detección
Los logs permiten detectar **síntomas directos**:

- errores de login
- fallos de sincronización
- timeouts específicos

## Limitación
No indican si el problema es aislado o sistémico.

👉 Por eso no se usan solos para decidir “hay problema”.

---

# 3. Métricas (estado agregado)

## Qué son
Valores numéricos agregados en el tiempo (series temporales).

## Qué aportan
- Visión global del comportamiento
- Tendencias
- Comparación contra baseline

## Por qué se usan en la detección
Permiten responder:

> “¿La escuela está funcionando peor que lo normal?”

Indicadores clave:
- error rate por `schoolId`
- latencia p95/p99
- throughput
- fallos de jobs

## Limitación
No explican el motivo del problema, solo su existencia.

👉 Detectan degradación, pero no causa.

---

# 4. Tracing (flujo del sistema)

## Qué es
Representación del recorrido completo de una request entre servicios.

## Qué aporta
- Visibilidad del flujo completo
- Identificación del punto exacto de fallo
- Medición de latencia por componente

## Por qué se usa en la detección
Permite responder:

> “¿Dónde se rompe el sistema para esta escuela?”

Ejemplo de análisis:
- DB lenta
- API externa fallando
- servicio interno degradado

## Limitación
Alto volumen de datos → requiere agregación y correlación.

---

# 5. Correlación por escuela (concepto clave)

## Qué significa
Todo evento del sistema debe estar etiquetado con:

- `schoolId`
- `requestId`
- `traceId`

## Por qué es crítico
Sin segmentación por tenant:
- solo ves salud global del sistema
- no podés detectar una escuela degradada aislada

Con segmentación:
- cada escuela se analiza como unidad independiente

---

# 6. Herramientas (implementación de observabilidad)

## Azure Application Insights
:contentReference[oaicite:0]{index=0}

### Rol
Correlación central de logs, métricas y tracing.

### Por qué se usa
- unifica señales
- permite análisis por request
- conecta servicios distribuidos

---

## Sentry
:contentReference[oaicite:1]{index=1}

### Rol
Detección y agrupación de errores.

### Por qué se usa
- detecta excepciones automáticamente
- agrupa errores repetidos
- permite ver regresiones por deploy

---

## Logging (Winston / Pino)

:contentReference[oaicite:2]{index=2}  
:contentReference[oaicite:3]{index=3}

### Rol
Generación de logs estructurados en backend.

### Por qué se usan
- performance en producción
- estructura JSON
- metadata por request (`schoolId`, `traceId`)

---

# 7. Cómo detectamos que una escuela tiene problemas

## Definición operativa
Una escuela tiene problemas cuando presenta **degradación sostenida y correlacionada en múltiples señales del sistema**.

---

## 7.1 Señales en logs (evento inmediato)
Detectan síntomas directos:

- errores repetidos por `schoolId`
- fallos de autenticación o sync
- timeouts recurrentes
- bursts de excepciones

---

## 7.2 Señales en métricas (estado agregado)
Detectan degradación sostenida:

- aumento de error rate
- latencia por encima del baseline
- caída de throughput
- fallos en jobs

---

## 7.3 Señales en tracing (causa estructural)
Detectan el origen:

- DB lenta
- servicio específico degradado
- dependencia externa fallando
- mismo span fallando repetidamente

---

## 7.4 Señales de silencio (caso crítico)
Detectan fallos invisibles:

- no llegan eventos esperados
- jobs no se ejecutan
- ausencia de tráfico esperado

---

## 7.5 Regla de decisión (core de la solución)

Una escuela se considera con problemas cuando:

> existe degradación en métricas + evidencia en logs + confirmación en tracing (o ausencia crítica de actividad)

👉 Ninguna señal individual es suficiente.

---

# 8. Flujo de detección operativo

```text
Request entra al sistema
↓
Se asigna schoolId + traceId
↓
Logs registran eventos
↓
Métricas agregan comportamiento
↓
Tracing reconstruye el flujo
↓
Sentry detecta excepciones
↓
Azure App Insights correlaciona todo
↓
Sistema evalúa desviaciones por schoolId
↓
Se detecta degradación del tenant
9. Conclusión (modelo mental correcto)

La detección de problemas en una escuela no es monitoreo aislado, sino:

Un proceso de correlación entre señales técnicas segmentadas por tenant que permite detectar degradación sostenida del comportamiento del sistema.

10. Idea clave final
Logs = evidencia puntual
Métricas = degradación cuantificada
Tracing = causa estructural
Correlación = decisión real

👉 El problema no se detecta con una señal, sino con la convergencia de las tres capas.