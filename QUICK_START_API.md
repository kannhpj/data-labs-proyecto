# Inicio Rápido - API de Predicción de Riesgo de Salud

Una guía rápida para ejecutar y probar la API en minutos.

## 1️⃣ Instalar dependencias (primera vez)

```bash
# Desde la raíz del proyecto
pip install -r requirements.txt

# O solo las dependencias de la API
cd api
pip install -r requirements_api.txt
cd ..
```

## 2️⃣ Ejecutar la API

```bash
cd api
python main.py
```

Deberías ver:
```
✓ Modelo cargado exitosamente desde: .../models/sk_auto_best_tuned.joblib
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

## 3️⃣ Acceder a la documentación interactiva

Abre en tu navegador:
```
http://localhost:8000/docs
```

Verás la documentación Swagger UI donde puedes:
- Ver todos los endpoints
- Leer descripción de parámetros
- **Probar directamente los endpoints**

## 4️⃣ Hacer tu primera predicción

### Opción A: Desde el navegador (Swagger UI)

1. Ve a http://localhost:8000/docs
2. Abre la sección `POST /predecir`
3. Click en "Try it out"
4. Modifica los valores si quieres
5. Click en "Execute"

### Opción B: Desde terminal con curl

```bash
curl -X POST "http://localhost:8000/predecir" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "weight": 75,
    "height": 175,
    "sleep": 7.5,
    "bmi": 24.5,
    "exercise": "medium",
    "sugar_intake": "medium",
    "smoking": "no",
    "alcohol": "no",
    "married": "yes",
    "profession": "office_worker"
  }'
```

### Opción C: Desde Python

```python
import requests

response = requests.post("http://localhost:8000/predecir", json={
    "age": 45,
    "weight": 75,
    "height": 175,
    "sleep": 7.5,
    "bmi": 24.5,
    "exercise": "medium",
    "sugar_intake": "medium",
    "smoking": "no",
    "alcohol": "no",
    "married": "yes",
    "profession": "office_worker"
})

print(response.json())
# Salida: {"health_risk": "low", "confidence": 0.87, "risk_level": "Bajo - Mantener estilos de vida saludables"}
```

## 5️⃣ Ejecutar pruebas automatizadas

En **otra terminal** (con la API corriendo):

```bash
cd api
python test_api.py
```

Verás todas las pruebas ejecutándose:
- ✓ Health Check
- ✓ Predicción de riesgo bajo
- ✓ Predicción de riesgo alto
- ✓ Predicciones en lote
- ✓ Y más...

## 📋 Parámetros Válidos

**Numéricos:**
- `age`: 18-100
- `weight`: 30-200 kg
- `height`: 100-250 cm
- `sleep`: 0-24 horas
- `bmi`: 10-60

**Categorías:**
- `exercise`: "low" | "medium" | "high"
- `sugar_intake`: "low" | "medium" | "high"
- `smoking`: "yes" | "no"
- `alcohol`: "yes" | "no"
- `married`: "yes" | "no"
- `profession`: "office_worker" | "teacher" | "artist" | "student" | "engineer" | "doctor" | "salesman" | "nurse"

## 🎯 Ejemplos de Predicciones

### Ejemplo 1: Riesgo Bajo (Persona joven y saludable)

```json
{
  "age": 30,
  "weight": 65,
  "height": 175,
  "sleep": 8.0,
  "bmi": 21.2,
  "exercise": "high",
  "sugar_intake": "low",
  "smoking": "no",
  "alcohol": "no",
  "married": "no",
  "profession": "engineer"
}
```

**Predicción esperada:** LOW (riesgo bajo)

### Ejemplo 2: Riesgo Alto (Persona con factores de riesgo)

```json
{
  "age": 65,
  "weight": 95,
  "height": 170,
  "sleep": 5.5,
  "bmi": 32.8,
  "exercise": "low",
  "sugar_intake": "high",
  "smoking": "yes",
  "alcohol": "yes",
  "married": "yes",
  "profession": "office_worker"
}
```

**Predicción esperada:** HIGH (riesgo alto)

## 🔗 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Verificar que API funciona |
| GET | `/ejemplo` | Obtener ejemplo de datos |
| GET | `/docs` | Documentación interactiva (Swagger) |
| GET | `/redoc` | Documentación alternativa (ReDoc) |
| POST | `/predecir` | Predecir para un paciente |
| POST | `/predecir-batch` | Predecir para múltiples pacientes |

## 📚 Documentación Completa

Para una documentación más detallada, consulta:

```bash
cat api/README.md
```

## ❌ Solución de Problemas

### "Connection refused" - Error de conexión

**Problema:** No puedes conectar a localhost:8000

**Solución:** Asegúrate de que la API está corriendo en otra terminal:
```bash
cd api && python main.py
```

### "El modelo no está cargado correctamente"

**Problema:** Error al cargar el modelo

**Solución:** Verifica que existe el archivo del modelo:
```bash
ls -lh models/sk_auto_best_tuned.joblib
```

### "Validation error" - Error de validación

**Problema:** El servidor rechaza tus datos

**Solución:** Verifica que:
- Los valores numéricos están en los rangos válidos
- Los valores categóricos son exactamente como se especifica (minúsculas)
- Todos los campos requeridos están presentes

### Puerto 8000 en uso

**Problema:** El puerto 8000 ya está ocupado

**Solución:** Usa otro puerto:
```bash
python main.py
# Ctrl+C para detener

# O ejecuta con un puerto diferente:
uvicorn main:app --port 8080
```

## 🚀 Próximos Pasos

1. **Integrar en tu aplicación** - Usa la API desde tu frontend/backend
2. **Desplegar** - Sube la API a un servidor en la nube
3. **Mejorar** - Entrena nuevos modelos y actualiza `sk_auto_best_tuned.joblib`

## 💡 Tips

- La documentación Swagger UI (http://localhost:8000/docs) es tu mejor amiga
- Todas las respuestas incluyen la confianza de la predicción
- La API valida automáticamente los datos de entrada
- Puedes procesar múltiples pacientes con `/predecir-batch`

---

¿Preguntas? Consulta el README.md completo en la carpeta `api/`.