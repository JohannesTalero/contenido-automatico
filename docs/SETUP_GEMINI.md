# 🔑 Configurar API de Gemini

Para usar el análisis con LLM en el notebook, necesitas una API key de Gemini (gratuita).

## Paso 1: Obtener API Key

1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en **"Get API Key"** o **"Create API Key"**
4. Copia la API key generada (empieza con `AIza...`)

## Paso 2: Configurar en Google Colab

### Opción A: Usar Secrets (Recomendado)

1. En tu notebook de Colab, haz clic en el ícono de **🔑 llave** en la barra lateral izquierda
2. Haz clic en **"Add new secret"**
3. Nombre: `GEMINI_API_KEY`
4. Valor: Pega tu API key
5. Activa el toggle para permitir acceso al notebook

El código del notebook automáticamente leerá la key:

```python
from google.colab import userdata
GEMINI_API_KEY = userdata.get('GEMINI_API_KEY')
```

### Opción B: Hardcodear (No recomendado - menos seguro)

⚠️ **Solo para testing rápido**. No compartas el notebook con la key visible.

```python
GEMINI_API_KEY = "AIza_TU_API_KEY_AQUI"
genai.configure(api_key=GEMINI_API_KEY)
```

## Paso 3: Verificar que Funciona

Ejecuta esta celda de prueba:

```python
import google.generativeai as genai
from google.colab import userdata

GEMINI_API_KEY = userdata.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Di hola en español")
print(response.text)
```

Si ves "Hola" o similar, ¡está funcionando! ✅

## Límites Gratuitos

Gemini 1.5 Flash (el modelo que usa el notebook) tiene límites generosos en el tier gratuito:

- **15 solicitudes por minuto**
- **1 millón de tokens por día**
- **1,500 solicitudes por día**

Para transcripciones típicas (1 hora de video ≈ 10K tokens), puedes procesar decenas de videos al día gratis.

## Alternativas

### Usar OpenAI GPT en vez de Gemini

Si prefieres usar GPT-4 o GPT-3.5:

1. Obtén API key en [OpenAI Platform](https://platform.openai.com/api-keys)
2. Instala: `%pip install openai`
3. Reemplaza la celda de configuración:

```python
from openai import OpenAI
from google.colab import userdata

client = OpenAI(api_key=userdata.get('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model="gpt-4o-mini",  # Más barato y rápido
    messages=[
        {"role": "system", "content": "Eres un experto editor de video."},
        {"role": "user", "content": prompt_analisis}
    ]
)

analisis_llm = response.choices[0].message.content
```

**Nota**: OpenAI es de pago desde el primer uso, pero GPT-4o-mini es muy económico (~$0.15 por millón de tokens de entrada).

## Troubleshooting

### Error: "API key not valid"
- Verifica que copiaste la key completa
- Revisa que el secret en Colab esté activado
- Regenera la key en AI Studio si es necesario

### Error: "Resource exhausted"
- Has alcanzado el límite de requests por minuto
- Espera 1 minuto y vuelve a intentar
- Considera usar un modelo más pequeño o dividir la transcripción

### Error: "USER_LOCATION_NOT_SUPPORTED"
- Gemini no está disponible en tu país aún
- Usa una VPN o cambia a OpenAI GPT

## Costo Estimado

### Gemini (Recomendado)
- **Costo**: $0 (gratis hasta 1M tokens/día)
- **Modelo**: gemini-1.5-flash
- **Velocidad**: ~2-5 segundos por análisis

### OpenAI GPT-4o-mini
- **Costo**: ~$0.01 - $0.02 por análisis de 1 hora de video
- **Modelo**: gpt-4o-mini
- **Velocidad**: ~3-8 segundos por análisis

### OpenAI GPT-4o
- **Costo**: ~$0.15 - $0.30 por análisis
- **Modelo**: gpt-4o (más inteligente)
- **Velocidad**: ~5-15 segundos por análisis

## ¿Necesitas Ayuda?

- [Documentación oficial de Gemini](https://ai.google.dev/docs)
- [Google AI Studio](https://aistudio.google.com/)
- [Pricing de Gemini](https://ai.google.dev/pricing)

