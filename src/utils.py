"""
Utilidades generales del proyecto.
"""

import torch
import sys
from pathlib import Path


def obtener_info_device():
    """
    Detecta el dispositivo disponible (GPU o CPU).
    
    Returns:
        dict con información del device
    """
    cuda_available = torch.cuda.is_available()
    
    if cuda_available:
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        
        return {
            "device": "cuda",
            "gpu_name": gpu_name,
            "gpu_memory_gb": round(gpu_memory, 2)
        }
    else:
        return {
            "device": "cpu",
            "gpu_name": None,
            "gpu_memory_gb": None
        }


def verificar_entorno():
    """
    Verifica el entorno de ejecución y muestra información.
    """
    info = obtener_info_device()
    es_colab = 'google.colab' in sys.modules
    
    print("=" * 60)
    print(f"Entorno: {'Google Colab' if es_colab else 'Local'}")
    print(f"Dispositivo: {info['device'].upper()}")
    if info['gpu_name']:
        print(f"GPU: {info['gpu_name']} ({info['gpu_memory_gb']} GB)")
    print("=" * 60)
    
    return info


def montar_drive():
    """Monta Google Drive si estamos en Colab."""
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        print("[+] Google Drive montado en /content/drive")
        return True
    except ImportError:
        return False


def formatear_tiempo(segundos):
    """
    Convierte segundos a formato HH:MM:SS.
    
    Args:
        segundos: float con los segundos
    
    Returns:
        str en formato HH:MM:SS
    """
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segs = segundos % 60
    return f"{horas:02d}:{minutos:02d}:{segs:06.3f}"
