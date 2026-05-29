# Prompt Tests

## Test 1 — Prompt básico

### Prompt usado

```txt
Explicá qué es JavaScript
```

### Respuesta obtenida

JavaScript es un lenguaje de programación usado principalmente para crear páginas web interactivas y dinámicas.

Con JavaScript podés hacer que una página:
- responda a clicks,
- actualice contenido sin recargar,
- valide formularios,
- muestre animaciones,
- maneje datos en tiempo real.

Funciona junto con:
- HTML → estructura,
- CSS → diseño,
- JavaScript → comportamiento y lógica.

### Qué cambió

La respuesta fue neutra y general.
El modelo dio una explicación estándar sin adaptar el contenido a un tipo específico de audiencia.


---

## Test 2 — Prompt con instrucciones

### Prompt usado

```txt
Explicá qué es JavaScript como si fuera para un niño de 10 años
```

### Respuesta obtenida

JavaScript es como una herramienta mágica que hace que las páginas web puedan moverse y reaccionar cuando las usás.

Por ejemplo, gracias a JavaScript:
- un botón puede hacer algo cuando lo tocás,
- una imagen puede moverse,
- un juego puede funcionar dentro de una página web.

Imaginá que:
- HTML es el esqueleto,
- CSS es la ropa,
- JavaScript es el cerebro.

### Qué cambió

La respuesta se volvió más simple y didáctica.
El modelo usó analogías, ejemplos concretos y lenguaje adaptado para un niño.
Disminuyó el nivel técnico para facilitar la comprensión.

---

## Test 3 — Prompt desordenado/malo

### Prompt usado

```txt
js que es rapido cosa web explicacion corta
```

### Respuesta obtenida

JavaScript es un lenguaje de programación usado para hacer páginas web interactivas y dinámicas. Permite agregar funciones como botones, animaciones y actualizaciones en tiempo real.

### Qué cambió

La respuesta fue más corta y menos estructurada.
El prompt estaba desordenado, pero el modelo pudo interpretar la intención general.
Se redujo la profundidad y claridad respecto a los prompts anteriores.

---

# Disclaimer sobre el uso de OpenAI Playground

No fue posible utilizar OpenAI Playground debido a un error de cuota de API relacionado con límites de facturación y uso de la plataforma OpenAI.

Error recibido:

```txt
You exceeded your current quota, please check your plan and billing details.
```

Debido a esta limitación, se decidió utilizar ChatGPT como entorno alternativo para realizar las pruebas de prompts y continuar con el aprendizaje práctico.

La decisión se tomó porque el objetivo principal de la actividad era analizar cómo cambian las respuestas de un modelo de lenguaje según el tipo de input recibido, y ChatGPT utiliza el mismo paradigma de modelos LLM basado en prompts e instrucciones contextuales.

Por lo tanto, el aprendizaje conceptual y experimental de la actividad pudo realizarse correctamente aunque no se utilizara directamente el Playground.

---

# Resumen final de aprendizaje

Esta actividad permitió comprender cómo los modelos de lenguaje interpretan y modifican sus respuestas según el contexto, estructura y claridad del prompt ingresado.

Durante las pruebas se observó que:

- Un prompt claro y neutro genera respuestas estándar y generales.
- Un prompt con instrucciones específicas modifica el tono, el nivel técnico y la forma pedagógica de la respuesta.
- Un prompt desordenado o ambiguo sigue siendo interpretado por el modelo gracias a su capacidad de inferencia semántica, aunque la calidad estructural disminuye.

También se entendió que los prompts funcionan como un sistema de control del comportamiento del modelo, permitiendo definir:
- audiencia,
- profundidad,
- formato,
- estilo,
- nivel técnico,
- objetivo de respuesta.

---

# Relación con el estudio de Agentes IA

Este ejercicio se realizó después de estudiar qué es un agente IA porque los prompts representan una de las bases fundamentales de los sistemas basados en modelos generativos.

Un agente IA no funciona únicamente por el modelo LLM, sino por cómo recibe instrucciones, interpreta contexto y toma decisiones utilizando entradas estructuradas.

Comprender cómo pequeños cambios en un prompt alteran el comportamiento del modelo es importante para:
- diseñar agentes,
- crear automatizaciones inteligentes,
- construir workflows,
- controlar herramientas,
- y desarrollar arquitecturas cognitivas más complejas.

Por este motivo, el estudio de Prompt Engineering fue utilizado como segundo paso dentro del proceso de aprendizaje de ICARUS.