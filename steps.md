## Plan Lean Startup para "Make Content" (Phymac)

### Principios guía
- Entregas pequeñas y utilizables: cada fase produce un entregable que se puede usar con material real (video + transcripción).
- Costos mínimos: priorizar open source (Whisper.cpp/faster-whisper, DeepFilterNet, ffmpeg, Remotion OSS). Servicios pagos solo como fallback barato (OpenAI Whisper API, GPT-4o-mini).
- Medir y aprender: en cada fase se definen señales de valor (tiempo ahorrado, claridad de narrativa, reutilización del JSON de metadatos).
- Flexibilidad técnico-pedagógica: soportar debates técnicos, pedagógicos e híbridos; privilegiar la narrativa "Challenge & Build" cuando aplique (lo que haré / lo que necesito / lo que aplico).

### Roadmap incremental (cada fase usable)

#### Fase 0 – Setup rápido (0.5 d)
- Estructura mínima de repo: `python/` (procesamiento), `js/` (render), `samples/` (1-2 videos cortos + transcripciones).
- Tooling gratuito: `ffmpeg`, `deepfilternet`, `faster-whisper` (CPU), `ollama` con Llama 3/4 mini para protos locales; `node + remotion` para capa visual.
- Entregable: script `python/ingest.py` que toma video+transcripción y guarda una copia limpia de audio (DeepFilterNet) + corte manual via timestamps.

#### Fase 1 – PoC de fin a fin manual-asistido (1-2 d)
- Input: video + transcripción provista.
- Proceso:
  - Limpieza de audio (DeepFilterNet) y normalización de volumen (ffmpeg).
  - Generar palabras con timestamps vía `faster-whisper` (si no hay transcripción alineada).
  - UI mínima (notebook o CLI) para marcar a mano los 2-5 minutos valiosos y seleccionar narrativa (Fail & Fix / Discovery & Learn / Debate & Decision / Challenge & Build / Iteration & Refinement).
  - Generar JSON de metadatos base:
    ```json
    {
      "narrativa": "...",
      "tipo_debate": "tecnico|pedagogico|hibrido",
      "etiquetas": [...],
      "segments": [{ "start": s, "end": e, "label": "[FAIL|ITERANDO|SUCCESS]" }],
      "palabras": [...]
    }
    ```
- Entregable: carpeta `output/` con audio limpio, video recortado (simple corte ffmpeg) y JSON. Usable ya para revisión.
- Métrica: ¿se puede producir un clip válido en <30 min con 1 persona?

#### Fase 2 – Automatizar detección de narrativa y momentos clave (2-3 d)
- Heurísticas + LLM ligero (ollama / GPT-4o-mini opcional) que:
  - Clasifica tipo de debate (técnico/pedagógico/híbrido).
  - Predice narrativa mejor fit (Fail & Fix / Discovery & Learn / Debate & Decision / Challenge & Build / Iteration & Refinement).
  - Extrae 2-3 "pepitas" (timestamps aproximados) y etiquetas por estado de narrativa.
- Ajustes manuales posibles vía CLI (`python/labeler.py --review`).
- Entregable: JSON enriquecido con narrativa y estados; corte automático preliminar de clips sugeridos.
- Métrica: precisión percibida >70% (los clips sugeridos están cerca de lo útil).

#### Fase 2.5 – Módulo de coherencia de contenido (1-2 d)
- Script `python/coherence.py` que analiza el contenido existente en `output/`:
  - Inventario de temas/conceptos cubiertos (extracción de keywords y conceptos clave de los JSON).
  - Balance de narrativas: detecta si hay exceso de "Fail & Fix" vs falta de "Challenge & Build" o viceversa.
  - Balance técnico/pedagógico: identifica gaps en contenido técnico vs pedagógico.
  - Sugerencias de contenido faltante:
    - Temas mencionados pero sin contenido dedicado.
    - Narrativas sub-representadas que deberían priorizarse.
    - Conceptos que requieren contenido complementario (ej. si hay muchos "Fail & Fix" técnicos, sugerir "Discovery & Learn" pedagógico).
- Salida: reporte JSON/Markdown con recomendaciones (`output/coherence_report.md`).
- Entregable: comando `python coherence.py --output output/` que genera reporte de gaps y sugerencias.
- Métrica: reporte generable en <30 segundos; recomendaciones accionables >80%.

#### Fase 3 – Generación editorial mínima (1-2 d)
- Plantillas de texto (Markdown) para:
  - Hilo X técnico, hilo X pedagógico, y Challenge & Build (lo que haré / lo que necesito / lo que aplico).
  - Resumen corto de blog.
- Relleno con metadatos + pocas llamadas LLM (gratis/local preferido).
- Entregable: `output/content/` con `thread.md` y `blog.md` por clip.
- Métrica: tiempo de edición humana <10 min por pieza.

#### Fase 4 – Capa visual inicial con Remotion (2-3 d)
- Theme Phymac aplicado: colores `#2962FF`, `#FF6D00`, fondo `#F5F5F5`, tipografía Montserrat/Open Sans (fuentes locales o Google Fonts).
- Subtítulos “karaoke” básicos con palabras + timestamps del JSON.
- Branding: overlay de logos + marco redondeado; barra de progreso acento naranja.
- Entregable: script `js/render.ts` que produce un MP4 corto (30-90s) por clip.
- Métrica: video renderizable en laptop sin GPU dedicada; legibilidad OK.

#### Fase 5 – Pipeline semi-automático (3-5 d)
- Orquestador simple (Makefile o CLI Python):
  - `ingest` → `clean_audio` → `transcribe` → `analyze` → `cut` → `render`.
  - Integración opcional de `coherence` para sugerir qué contenido crear antes de procesar nuevos debates.
- Caché de pasos para no recalcular (p. ej. guardar embeddings y ASR).
- Soporte batch de varios debates en `input/`.
- Entregable: comando único `python run.py --input input/video.mp4 --transcript input.txt`.
- Métrica: throughput ≥3 debates/hora en máquina local.

#### Fase 6 – Calidad y DX (2-3 d)
- Tests básicos de funciones puras (narrativa, formateo de hilos).
- Lints/formatters (`ruff`, `black`, `eslint`, `prettier`).
- Presets de prompts versionados (`prompts/*.md`) para reproducibilidad.
- Métrica: tiempo de setup para nuevo colaborador <30 min.

#### Fase 7 – Opcional: mejoras pro (post-MVP)
- Detección de “hands-on” (screen-share/code) con detección de UI luminancia + OCR ligero.
- Modelos de diarización para múltiples voces (pyannote) si el audio mejora.
- Integración S3/local para assets; dashboard web ligero para revisión y edición rápida.

### Costos y stack recomendados (mínimo gasto)
- ASR: `faster-whisper` CPU (gratis); fallback Whisper API barato para cargas grandes.
- LLM: `ollama` (Llama 3/4 mini) local; fallback GPT-4o-mini para mejor calidad puntual.
- Audio: `DeepFilterNet` + `ffmpeg` (gratis).
- Video: `ffmpeg` + `remotion` (gratis).
- Infra: correr en laptop/PC; usar almacenamiento local o bucket S3 económico solo si necesario.

### Proceso de trabajo con videos reales
1) Recibimos video + transcripción (si no, se genera).
2) Ejecutar pipeline de la fase alcanzada; revisar JSON y cortes propuestos.
3) Ajustar manualmente si es necesario; regenerar hilos y render.
4) Recoger feedback (claridad narrativa, fidelidad al debate, estética Phymac).
5) Iterar a siguiente fase solo si el entregable actual ya se usa con valor.

### Próximos pasos inmediatos (Fase 0 → 1)
- Crear estructura de carpetas y scripts vacíos.
- Incluir 1-2 videos de prueba (in-house) y transcripciones para iterar.
- Implementar ingest + limpieza + corte manual y generación de JSON base.
- Documentar comandos rápidos en `README`/`Makefile`.

### Módulos pendientes de implementación
- `python/labeler.py`: CLI para revisar y ajustar narrativas y etiquetas (Fase 2).
- `python/coherence.py`: Módulo de análisis de coherencia de contenido (Fase 2.5).
- `python/editorial.py`: Generación de hilos y blogs (Fase 3).
- `js/render.ts`: Renderizado visual con Remotion (Fase 4).
- `python/run.py`: Orquestador del pipeline completo (Fase 5).

