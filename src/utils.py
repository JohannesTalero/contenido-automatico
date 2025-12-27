import torch
import sys
import os
from pathlib import Path

def get_device_info():
    """
    Detecta el dispositivo disponible (GPU o CPU) y retorna información útil.
    """
    cuda_available = torch.cuda.is_available()
    device = "cuda" if cuda_available else "cpu"
    
    if cuda_available:
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
        
        # Para GPUs con poca memoria (< 6GB), usar int8_float16
        if gpu_memory < 6:
            compute_type = "int8_float16"
        else:
            compute_type = "float16"
        
        return {
            "device": device,
            "gpu_name": gpu_name,
            "gpu_memory_gb": round(gpu_memory, 2),
            "compute_type": compute_type
        }
    else:
        return {
            "device": device,
            "gpu_name": None,
            "gpu_memory_gb": None,
            "compute_type": "int8"
        }

def clear_gpu_memory():
    """Limpia la memoria de la GPU si está disponible."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

def setup_colab_drive():
    """Configura el montaje de Google Drive si estamos en Colab."""
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        return True
    except ImportError:
        return False

def get_drive_path(relative_path=""):
    """Retorna la ruta completa en Google Drive si está disponible."""
    base_drive = Path("/content/drive/MyDrive/contenido-automatico")
    if relative_path:
        return base_drive / relative_path
    return base_drive

def check_env():
    """Verifica el entorno de ejecución."""
    info = get_device_info()
    print("=" * 60)
    print(f"Entorno: {'Google Colab' if 'google.colab' in sys.modules else 'Local'}")
    print(f"Dispositivo: {info['device'].upper()}")
    if info['gpu_name']:
        print(f"GPU: {info['gpu_name']} ({info['gpu_memory_gb']} GB)")
    print(f"Compute Type: {info['compute_type']}")
    print("=" * 60)
    return info
