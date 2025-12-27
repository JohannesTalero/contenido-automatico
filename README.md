# 🎬 Make Content (Phymac) - MVP

Este proyecto automatiza la transformación de debates técnicos y pedagógicos en contenido de micro-aprendizaje. Optimizado para ejecutarse en **Google Colab** usando GPU gratuita.

## 🚀 Inicio Rápido (Google Colab)

La forma más fácil de usar este proyecto es a través de Google Colab, lo que evita problemas de hardware local y falta de memoria en GPU.

1. **Abrir Notebook**: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](notebooks/procesar_contenido.ipynb)
2. **Sube tu video** a tu Google Drive en la carpeta `contenido-automatico/input/`.
3. **Ejecuta el notebook** siguiendo las instrucciones integradas.

## 📁 Estructura del Proyecto

```
contenido-automatico/
├── src/                  # Código fuente (Python)
│   ├── ingest.py        # Pipeline principal (Limpieza + Transcripción + Corte)
│   └── utils.py         # Utilidades de GPU y Google Drive
├── notebooks/            # Notebooks listos para Google Colab
├── docs/                 # Documentación detallada y guías
├── config/               # Archivos de configuración
└── samples/              # Videos de ejemplo (Ignorados en GitHub si son pesados)
```

## 🛠️ Instalación Local (Opcional)

Si prefieres ejecutarlo localmente y tienes una GPU NVIDIA potente (mínimo 6GB VRAM):

1. **Requisitos**: Python 3.10+, FFmpeg.
2. **Clonar y configurar**:
   ```bash
   git clone https://github.com/TU_USUARIO/contenido-automatico.git
   cd contenido-automatico
   python -m venv venv
   source venv/bin/activate  # o venv\Scripts\activate en Windows
   pip install -r src/requirements.txt
   ```
3. **Ejecutar**:
   ```bash
   python -m src.ingest samples/tu_video.mp4 --start 00:01:00 --end 00:03:30
   ```

## 📦 Manejo de Archivos Pesados

Este repositorio está configurado para **NO subir archivos pesados** (videos, audios grandes) a GitHub. 
- Usa **Google Drive** como almacenamiento para tus videos de entrada y resultados.
- El notebook de Colab gestiona la conexión con Drive automáticamente.

## 📄 Documentación

- [Guía de Configuración en Colab](docs/SETUP_COLAB.md)
- [Opciones de GPU en la Nube](docs/CLOUD_GPU_OPTIONS.md)
- [Plan de Desarrollo](steps.md)

---
Desarrollado para la **Fundación Phymac** - Aprendizaje por retos.
