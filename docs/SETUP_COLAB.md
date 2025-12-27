# Guía Rápida: Procesar en Cloud

## 🎯 Opción Recomendada: Kaggle (Gratis)

### Paso 1: Preparar archivos localmente

```bash
cd python
python ingest_cloud.py ../samples/sesion_1.mp4 --provider kaggle --start 00:01:00 --end 00:03:30
```

Esto generará:
- `output/cloud_kaggle_script.py` - Script para ejecutar en Kaggle
- `output/INSTRUCCIONES_KAGGLE.md` - Instrucciones detalladas

### Paso 2: Subir a Kaggle

1. Ve a [kaggle.com](https://kaggle.com) y crea cuenta (gratis)
2. Crea un nuevo notebook:
   - Click en "New Notebook"
   - En "Settings" → "Accelerator" → Selecciona **"GPU"**
3. Sube archivos:
   - Click en "Add Data" → "Upload"
   - Sube: `samples/sesion_1.mp4`
   - Sube: `python/ingest.py`
   - Sube: `output/cloud_kaggle_script.py`

### Paso 3: Ejecutar en Kaggle

En el notebook, ejecuta:

```python
# Instalar dependencias
!pip install -q faster-whisper deepfilternet click torch torchaudio

# Ejecutar procesamiento
exec(open('cloud_kaggle_script.py').read())
```

### Paso 4: Descargar resultados

1. Los archivos estarán en la carpeta `output/`
2. Click derecho → Download en cada archivo:
   - `*_clean.wav`
   - `*_cut.mp4`
   - `*_meta.json`

---

## 💰 Alternativa: RunPod (Muy Económico)

### Setup inicial

1. Crear cuenta en [runpod.io](https://runpod.io)
2. Agregar créditos ($5-10 es suficiente para empezar)
3. Crear pod:
   - Template: "PyTorch"
   - GPU: RTX 3090 ($0.29/hora)
   - Click "Deploy"

### Conectar y procesar

```bash
# Conectar via SSH (RunPod te da la IP)
ssh root@<IP>

# Clonar tu repo o subir archivos
git clone <tu-repo>
# o usar scp para subir archivos

# Ejecutar
cd contenido-automatico/python
python ingest.py ../samples/sesion_1.mp4 --start 00:01:00 --end 00:03:30
```

### Descargar resultados

```bash
# Desde tu máquina local
scp root@<IP>:/path/to/output/* ./output/
```

---

## ⚡ Solución Híbrida (Recomendada para producción)

**Estrategia**: 
- Procesar transcripción localmente (CPU funciona bien)
- Solo usar cloud para DeepFilterNet cuando sea necesario

### Script híbrido

```python
# Procesar transcripción local (rápido en CPU)
python ingest.py video.mp4 --skip-clean --start 00:01:00 --end 00:03:30

# Luego, solo limpieza en cloud si es necesario
# (puedes hacer esto manualmente o automatizarlo)
```

---

## 📊 Costos Estimados

| Escenario | Costo/mes |
|-----------|-----------|
| Kaggle (gratis) | $0 |
| RunPod (2-3 horas/mes) | ~$0.60 |
| Híbrido (solo limpieza en cloud) | ~$0.20 |

---

## 🆘 Troubleshooting

### Kaggle se desconecta
- Guarda resultados frecuentemente
- Usa checkpoints si procesas archivos largos

### RunPod se queda sin créditos
- Configura alertas de gasto
- Usa "Spot" instances para ahorrar

### Archivos muy grandes
- Comprime antes de subir
- Procesa en chunks más pequeños

