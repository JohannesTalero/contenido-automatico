# Documento de Contexto Técnico: Proyecto "Make Content"

## 0. Contexto Organizacional: Fundación Phymac

Este proyecto está desarrollado para la **Fundación Phymac** ([phymac.com](https://phymac.com/)), una organización que promueve el aprendizaje por retos para entender el mundo tecnológico.

### Misión y Metodología de Phymac
- **Enfoque:** Aprendizaje por retos - descubrir la ciencia construyendo artefactos para resolver problemas reales
- **Método STEM:** Ciclo de tres fases:
  1. **Lo que haré** - Definición del reto/problema
  2. **Lo que necesito** - Identificación de recursos y conocimientos requeridos
  3. **Lo que aplico** - Implementación práctica y resolución
- **Filosofía:** Combinar ingenio, lúdica y retos para fomentar el descubrimiento continuo
- **Aplicación:** Aprendizaje práctico en cualquier nivel educativo

### Alineación del Proyecto con Phymac
El sistema "Make Content" debe reflejar y amplificar estos valores:
- **Contenido basado en retos reales:** Los debates del equipo (técnicos y pedagógicos) representan problemas reales que se resuelven en tiempo real
- **Aprendizaje práctico:** El contenido generado debe mostrar el proceso de "hacer" y no solo la teoría
- **Enfoque lúdico:** La estética visual "eléctrica y vibrante" debe mantener el espíritu lúdico de Phymac
- **Metodología STEM visible:** Cuando sea posible, estructurar el contenido siguiendo las tres fases (lo que haré, lo que necesito, lo que aplico)

**Pregunta:** ¿Debería el sistema poder identificar y etiquetar explícitamente estas tres fases en los debates para generar contenido que siga la metodología Phymac?

---

## 1. Visión General

Transformar los debates técnicos, pedagógicos y sesiones de "brainstorming" del equipo (desarrolladores y profesores) en contenido de micro-aprendizaje. El sistema debe capturar el **caos creativo** de una discusión técnica o educativa y estructurarlo bajo múltiples narrativas posibles (ej. **"Fail & Fix"**, **"Discovery & Learn"**, **"Debate & Decision"**, etc.), aplicando una capa visual eléctrica y vibrante.

**Aclaración:** El equipo no es exclusivamente técnico. Incluye profesores que discuten sobre diseño de programas educativos, evaluación de viabilidad pedagógica, decisiones sobre qué enseñar y cómo estructurar el contenido. Estas discusiones pedagógicas son tan valiosas como las técnicas para generar contenido.

## 2. Definición de Capas y Stack

### A. Capa de Análisis y Contextualización (LLM - Lila)

Dado que el input son debates internos (técnicos y pedagógicos), el LLM (Python + LangChain) tiene una tarea extra:

* **Limpieza de Jerga:** Identificar términos internos (ej. "el bug del viernes en el deploy 4" o "ese módulo que discutimos en la reunión de diseño") y convertirlos en conceptos universales (ej. "problemas de concurrencia en producción" o "diseño de currículo basado en competencias").
* **Extracción de la Pepita de Oro:** En un debate de 60 min, el LLM debe localizar los 2-5 min donde se resolvió el problema técnico real, se tomó una decisión pedagógica clave, o se llegó a un insight valioso.
* **Identificación de Narrativa:** El LLM debe detectar qué tipo de narrativa se ajusta mejor al debate:
  - **"Fail & Fix"**: Error técnico/pedagógico identificado y solución encontrada.
  - **"Discovery & Learn"**: Exploración de nuevas tecnologías, metodologías o enfoques educativos.
  - **"Debate & Decision"**: Discusión sobre si vale la pena implementar algo, qué enfoque tomar, o cómo estructurar un programa.
  - **"Iteration & Refinement"**: Mejora continua de un proceso, código o diseño educativo.
  - **"Challenge & Build"**: Reto definido y resolución siguiendo el método STEM de Phymac (lo que haré, lo que necesito, lo que aplico). Ideal para debates sobre diseño de retos educativos o construcción de soluciones paso a paso.
  - *¿Qué otras narrativas podrían ser útiles para el equipo?*
* **Estructuración según Narrativa:** Una vez identificada la narrativa, estructurar el contenido según su formato específico (ej. para "Fail & Fix": definir qué fue el "Ups..." y cuál fue el "¡Boom!").

### B. Capa de Procesamiento de Media (Python - Azul)

* **Audio "Studio Quality":** Usar **DeepFilterNet** para que una grabación de sala de juntas o Meet suene como un podcast profesional.
* **Video High Key:** Aplicar filtros de exposición para que el código en pantalla, las caras de los devs/profesores, o las presentaciones/diagramas se vean nítidas y brillantes (estética de laboratorio).
* **Detección de "Hands-on":** Script para detectar cuando se comparte pantalla (código, diagramas, presentaciones educativas) y priorizar esos clips en los Shorts.
* **Aclaración:** No todos los debates incluyen código. Algunos son discusiones pedagógicas sobre diseño de programas, metodologías, o decisiones estratégicas. El sistema debe poder generar contenido valioso incluso cuando no hay código visible.

### C. Capa de Estética y Subtitulado (JavaScript - Azul)

* **Tecnología:** Node.js con **Remotion**.
* **Subtítulos "Power Up":** * Fuente: **Montserrat ExtraBold**.
* Animación: Estilo "Karaoke" con los colores de marca: `#F5F5F5` (base), `#2962FF` (resaltado técnico), `#FF6D00` (palabras de acción/gritos).


* **Branding:** Superposición automática de logos de **Phymac** y marcos con bordes redondeados. El branding debe reflejar la identidad visual de la fundación y mantener coherencia con su presencia digital.

---

## 3. Identidad Visual: Kit de Phymac

El equipo de desarrollo debe configurar el motor de renderizado con estas variables constantes, alineadas con la identidad visual de Phymac:

| Elemento | Valor Técnico | Uso |
| --- | --- | --- |
| **Color Primario** | `#2962FF` | Subtítulos de términos técnicos y conceptos pedagógicos clave. |
| **Color Acento** | `#FF6D00` | Resaltado de soluciones ("The Fix"), decisiones finales, o insights clave. |
| **Fondo / Texto** | `#F5F5F5` / `#212121` | Contraste máximo para legibilidad. |
| **Tipografía Títulos** | Montserrat ExtraBold | Para "títulos que gritan" en portadas de Shorts. |
| **Tipografía Cuerpo** | Open Sans | Para hilos de Twitter y Blogs. |

**Aclaración:** Los colores y tipografías deben aplicarse consistentemente independientemente del tipo de debate (técnico o pedagógico) para mantener la identidad de marca. Sin embargo, los elementos visuales específicos (iconos, ilustraciones) pueden variar según la narrativa seleccionada.

**Pregunta:** ¿Deberían los contenidos pedagógicos tener algún elemento visual distintivo (ej. iconos de educación, diagramas de flujo) que los diferencie de los técnicos, o mantener un estilo completamente unificado?

---

## 4. Rama Editorial: De Debate a Contenido (X/Twitter)

El flujo para Twitter (X) es crítico. El LLM debe generar hilos que no parezcan actas de reunión, sino lecciones:

**Para debates técnicos:**
1. **Tweet Hook:** "Hoy casi rompemos producción por un error de [Concepto]. Así lo arreglamos ⚡"
2. **Cuerpo:** 3-4 tweets explicando el "Diagnóstico" con capturas del video (generadas por el script de Python).
3. **Cierre:** El "Hack" final y link al blog completo.

**Para debates pedagógicos:**
1. **Tweet Hook:** "Discutimos si vale la pena enseñar [Concepto] en el programa. Esta fue nuestra decisión y por qué 🎓"
2. **Cuerpo:** 3-4 tweets explicando el debate, las opciones consideradas, y la decisión final con sus razones.
3. **Cierre:** El insight clave y link al blog completo.

**Para contenido siguiendo metodología Phymac (Challenge & Build):**
1. **Tweet Hook:** "Diseñamos un reto para enseñar [Concepto]. Así lo estructuramos siguiendo nuestro método ⚡"
2. **Cuerpo:** 
   - Tweet 1: "Lo que haré" - El reto definido
   - Tweet 2: "Lo que necesito" - Recursos y conocimientos requeridos
   - Tweet 3: "Lo que aplico" - La solución construida
3. **Cierre:** Invitación a aceptar el reto y link al contenido completo.

**Pregunta:** ¿Deberían los hilos pedagógicos tener un formato diferente o seguir la misma estructura que los técnicos? ¿Cómo destacar mejor el enfoque de "aprendizaje por retos" de Phymac en el contenido generado?

---

## 5. Módulo de Coherencia de Contenido

El sistema debe incluir un módulo dedicado a analizar y mantener la coherencia del contenido generado. Este módulo (`python/coherence.py`) es crítico para asegurar que la biblioteca de contenido de Phymac sea balanceada, completa y coherente.

### Funcionalidades del Módulo de Coherencia

1. **Análisis de Inventario de Contenido:**
   - Escanea todos los JSON de metadatos en `output/` para extraer:
     - Temas y conceptos clave mencionados (usando extracción de keywords y análisis de transcripciones).
     - Narrativas utilizadas (Fail & Fix, Discovery & Learn, Challenge & Build, etc.).
     - Tipos de debate (técnico, pedagógico, híbrido).
     - Conceptos que aparecen como "mencionados" pero sin contenido dedicado.

2. **Detección de Desequilibrios:**
   - **Balance de Narrativas:** Identifica si hay exceso de una narrativa (ej. muchos "Fail & Fix") y falta de otras (ej. pocos "Challenge & Build").
   - **Balance Técnico/Pedagógico:** Detecta si el contenido está sesgado hacia lo técnico o lo pedagógico.
   - **Cobertura Temática:** Identifica temas que requieren más profundidad o contenido complementario.

3. **Sugerencias de Contenido Faltante:**
   - **Gaps Temáticos:** Conceptos mencionados en debates pero sin contenido dedicado que los explique.
   - **Narrativas Sub-representadas:** Sugiere qué narrativas deberían priorizarse para balancear el contenido.
   - **Contenido Complementario:** Si hay muchos "Fail & Fix" técnicos, sugiere crear "Discovery & Learn" pedagógicos o viceversa.
   - **Seguimiento de Conceptos:** Identifica conceptos que aparecen en múltiples debates pero no tienen un contenido central que los unifique.

4. **Reporte de Coherencia:**
   - Genera un reporte en Markdown (`output/coherence_report.md`) con:
     - Resumen estadístico de narrativas y tipos de debate.
     - Lista de gaps identificados con prioridad.
     - Recomendaciones accionables de qué contenido crear.
     - Sugerencias de debates existentes que podrían generar contenido complementario.

### Integración en el Flujo de Trabajo

- **Antes de procesar nuevos debates:** Ejecutar `python coherence.py` para ver qué gaps existen y priorizar qué debates procesar.
- **Después de generar contenido:** Re-ejecutar para actualizar el análisis y detectar nuevos gaps.
- **Planificación de contenido:** Usar el reporte para planificar qué tipo de debates grabar o qué contenido crear.

### Alineación con Metodología Phymac

El módulo de coherencia debe asegurar que:
- El contenido refleje el balance entre las diferentes narrativas, especialmente privilegiando "Challenge & Build" cuando sea apropiado.
- Los conceptos técnicos y pedagógicos estén representados de manera equilibrada.
- Los temas mencionados tengan contenido dedicado que los explique y contextualice.
- La biblioteca de contenido forme un ecosistema coherente donde los conceptos se refuercen mutuamente.

---

## 6. Requerimientos de Integración (Python ↔ JS)

Para que los desarrolladores de Python y JS trabajen en sintonía, el **punto de unión** será un servidor de archivos (S3/Local) y un JSON de metadatos:

1. **Python** entrega: Video recortado + Audio limpio + JSON de palabras con timestamps + **metadatos de narrativa identificada** (ej. `{"narrativa": "Fail & Fix", "etiquetas": ["FAIL", "ITERANDO", "SUCCESS"], "timestamps": {...}}`).
2. **JS (Node)** recibe: Los assets de Python y aplica la capa de diseño (subtítulos animados, barras de progreso de color naranja, transiciones de rayo) **ajustándose al estilo visual de la narrativa identificada**.

**Aclaración:** El JSON de metadatos debe incluir información sobre el tipo de debate (técnico vs. pedagógico) y la narrativa seleccionada para que la capa de JS pueda adaptar el estilo visual y los elementos gráficos apropiados.

---

## 7. Estilos de Narrativa: Múltiples Formatos

El sistema debe identificar y aplicar la narrativa más adecuada según el tipo de debate. Cada narrativa tiene sus propios estados/etiquetas para facilitar el montaje:

### Narrativa "Fail & Fix" (Error y Solución)
* **[FAIL]:** Frustración, duda, explicación del problema técnico o pedagógico.
* **[ITERANDO]:** "Manos a la obra", código moviéndose, discusión técnica/pedagógica intensa.
* **[SUCCESS]:** "¡Boom! Funcionó", alegría del equipo, solución implementada o decisión tomada.

### Narrativa "Discovery & Learn" (Descubrimiento y Aprendizaje)
* **[EXPLORANDO]:** Investigación, pruebas, experimentación con nuevas tecnologías o metodologías.
* **[INSIGHT]:** Momento de comprensión, "ajá", descubrimiento clave.
* **[APLICANDO]:** Implementación del aprendizaje, integración en el proyecto o programa.

### Narrativa "Debate & Decision" (Debate y Decisión)
* **[PROBLEMA]:** Presentación del dilema o pregunta a resolver (ej. "¿Vale la pena enseñar X?").
* **[ARGUMENTOS]:** Discusión de pros y contras, diferentes perspectivas del equipo.
* **[DECISIÓN]:** Conclusión, decisión final y justificación.

### Narrativa "Challenge & Build" (Reto y Construcción) - Metodología Phymac
Esta narrativa sigue explícitamente el ciclo STEM de tres fases de Phymac:
* **[LO QUE HARÉ]:** Definición del reto, problema o objetivo a resolver. Presentación clara del desafío.
* **[LO QUE NECESITO]:** Identificación de recursos, conocimientos, herramientas o conceptos requeridos para abordar el reto.
* **[LO QUE APLICO]:** Implementación práctica, construcción del artefacto o solución, y resolución del problema.

**Aclaración:** Esta narrativa es especialmente valiosa para debates pedagógicos sobre diseño de programas o retos educativos, pero también puede aplicarse a retos técnicos donde se construye una solución paso a paso.

### Narrativa "Iteration & Refinement" (Iteración y Refinamiento)
* **[INICIAL]:** Estado inicial del proceso, código o diseño educativo.
* **[MEJORANDO]:** Identificación de áreas de mejora, experimentación con cambios.
* **[REFINADO]:** Versión mejorada, lecciones aprendidas, y optimización final.

**Preguntas para el equipo:**
- ¿Qué otras narrativas serían útiles para capturar diferentes tipos de debates?
- ¿Debería el sistema poder combinar narrativas en un mismo contenido?
- ¿Cómo manejar debates que no encajan claramente en ninguna narrativa predefinida?

---

## 8. Preguntas Abiertas y Consideraciones

### Preguntas Técnicas
- ¿Cómo debe el sistema manejar debates híbridos que combinan aspectos técnicos y pedagógicos?
- ¿Debería haber diferentes estilos visuales para cada tipo de narrativa, o mantener un estilo consistente?
- ¿Cómo priorizar qué debates generar como contenido? ¿Basado en engagement potencial, valor educativo, o ambos?

### Preguntas de Contenido
- ¿Qué tan detallado debe ser el contenido generado? ¿Micro-aprendizaje de 2-3 min o contenido más extenso?
- ¿Debería el sistema generar contenido para diferentes audiencias (estudiantes, otros educadores, desarrolladores)?
- ¿Cómo manejar debates donde no se llegó a una conclusión clara o donde hay desacuerdos en el equipo?

### Preguntas de Narrativa
- ¿Debería el sistema poder sugerir múltiples narrativas para un mismo debate y dejar que el usuario elija?
- ¿Cómo etiquetar debates que son más conversacionales y menos estructurados?
- ¿Qué hacer con debates que son principalmente administrativos o de planificación sin valor educativo directo?

### Aclaraciones Importantes
- **Contexto Phymac:** Todo el contenido generado debe alinearse con la misión de Phymac: aprendizaje por retos, enfoque práctico, y metodología STEM. El contenido debe inspirar a otros a "aceptar el reto" y aprender construyendo.
- **Equipo Multidisciplinario:** El sistema debe reconocer que el equipo incluye tanto desarrolladores como educadores, y que ambos tipos de discusiones son valiosas para generar contenido educativo.
- **Flexibilidad de Narrativas:** No todos los debates encajan en "Fail & Fix". El sistema debe ser flexible y poder identificar y aplicar la narrativa más apropiada, incluyendo la narrativa "Challenge & Build" que refleja directamente la metodología Phymac.
- **Valor Educativo:** El objetivo no es solo documentar, sino crear contenido educativo que otros puedan aprender y aplicar. Esto aplica tanto para decisiones técnicas como pedagógicas, siempre con el enfoque de resolver retos reales.
- **Metodología STEM Visible:** Cuando sea posible, el contenido debe estructurarse o etiquetarse siguiendo las tres fases de Phymac (lo que haré, lo que necesito, lo que aplico) para reforzar el método de aprendizaje por retos.
- **Coherencia de Contenido:** El sistema debe incluir un módulo de análisis de coherencia que:
  - Analice el contenido existente para identificar gaps temáticos y narrativos.
  - Sugiera qué tipo de contenido nuevo crear para mantener balance entre narrativas (Fail & Fix, Discovery & Learn, Challenge & Build, etc.).
  - Detecte desequilibrios entre contenido técnico y pedagógico.
  - Identifique conceptos mencionados pero sin contenido dedicado que requieren seguimiento.
  - Proporcione recomendaciones accionables para mantener una biblioteca de contenido coherente y completa.

---

### ¿Cómo quieres proceder?

Puedo redactar el **"System Prompt"** definitivo que usará el LLM para procesar los debates internos (técnicos y pedagógicos) de Phymac, asegurándome de que sepa cómo:
- Identificar el tipo de debate (técnico, pedagógico, híbrido)
- Seleccionar la narrativa más apropiada (incluyendo "Challenge & Build" cuando corresponda)
- Extraer el contexto valioso alineado con la metodología de aprendizaje por retos de Phymac
- Convertirlo en el formato adecuado según la narrativa elegida (que puede variar según el tipo de contenido)
- Mantener el enfoque de Phymac: resolver retos reales, aprendizaje práctico, y metodología STEM visible