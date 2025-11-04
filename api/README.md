# API de Predicción de Riesgo de Salud

Una API simple y poderosa basada en **FastAPI** para predecir el nivel de riesgo de salud de pacientes usando un modelo de Machine Learning entrenado con AutoML.

## Características

- ✅ **Predicción individual** - Envía datos de un paciente y obtén su riesgo
- ✅ **Predicciones en lote** - Procesa múltiples pacientes a la vez
- ✅ **Validación automática** - Valida rangos y tipos de datos
- ✅ **Documentación interactiva** - Swagger UI integrada
- ✅ **Modelo optimizado** - Usa el mejor modelo entrenado (XGBoost tuned)
- ✅ **Confianza de predicción** - Devuelve probabilidades para cada predicción

## Requisitos

- Python 3.13+
- FastAPI
- Uvicorn
- Scikit-learn
- Pandas
- Joblib
- Requests (solo para pruebas)

## Instalación

### 1. Instalar dependencias (ya están en requirements.txt)

```bash
pip install fastapi uvicorn scikit-learn pandas joblib requests
```

O si estás en la raíz del proyecto:

```bash
pip install -r requirements.txt
```

## Ejecución

### Opción 1: Ejecutar directamente

```bash
cd api
python main.py
```

Verás:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Opción 2: Con uvicorn (con recarga automática)

```bash
cd api
uvicorn main:app --reload
```

### Opción 3: Especificar puerto diferente

```bash
python main.py --port 8080
# O
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Acceso a la API

Una vez que la API esté corriendo:

### 📚 Documentación Interactiva

**Swagger UI:** http://localhost:8000/docs

Aquí puedes:
- Ver todos los endpoints
- Leer la documentación automática
- **Probar los endpoints directamente en el navegador**
- Ver esquemas de entrada y salida

### 🔧 Alternativa con Redoc

**ReDoc:** http://localhost:8000/redoc

Documentación en formato alternativo.

## Endpoints

### 1. GET `/` - Información General

Devuelve información sobre la API.

```bash
curl http://localhost:8000/
```

### 2. GET `/health` - Health Check

Verifica que la API esté funcionando y que el modelo está cargado.

```bash
curl http://localhost:8000/health
```

### 3. GET `/ejemplo` - Ejemplo de Datos

Devuelve un ejemplo de cómo usar la API con valores válidos.

```bash
curl http://localhost:8000/ejemplo
```

### 4. POST `/predecir` - Predicción Individual ⭐

Predice el riesgo de salud para un paciente.

**Entrada (JSON):**
```json
{
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
}
```

**Ejemplo con curl:**
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

**Salida (JSON):**
```json
{
  "health_risk": "low",
  "confidence": 0.87,
  "risk_level": "Bajo - Mantener estilos de vida saludables"
}
```

### 5. POST `/predecir-batch` - Predicciones en Lote

Predice para múltiples pacientes a la vez.

**Entrada:**
```json
[
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
  },
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
]
```

## Parámetros Válidos

### Valores Numéricos
- **age**: 18-100 años
- **weight**: 30-200 kg
- **height**: 100-250 cm
- **sleep**: 0-24 horas
- **bmi**: 10-60 (índice de masa corporal)

### Valores Categóricos
- **exercise**: `low`, `medium`, `high`
- **sugar_intake**: `low`, `medium`, `high` (opcional, default: `medium`)
- **smoking**: `yes`, `no`
- **alcohol**: `yes`, `no`
- **married**: `yes`, `no`
- **profession**: `office_worker`, `teacher`, `artist`, `student`, `engineer`, `doctor`, `salesman`, `nurse`

## Pruebas Automatizadas

### Ejecutar el script de pruebas

1. **Asegúrate de que la API está corriendo** en otra terminal:
   ```bash
   cd api
   python main.py
   ```

2. **En otra terminal, ejecuta las pruebas:**
   ```bash
   cd api
   python test_api.py
   ```

### Qué pruebas se ejecutan

1. ✓ Health Check - Verifica que la API está activa
2. ✓ Información - Obtiene info de la API
3. ✓ Ejemplo de datos - Descarga ejemplo
4. ✓ Predicción - Riesgo Bajo - Paciente joven y saludable
5. ✓ Predicción - Riesgo Alto - Paciente con factores de riesgo
6. ✓ Predicciones en Lote - Múltiples pacientes
7. ✓ Validación de Errores - Rechaza datos inválidos

**Output esperado:**
```
╔══════════════════════════════════════════════════════════╗
║ PRUEBAS DE LA API DE PREDICCIÓN DE RIESGO DE SALUD        ║
╚══════════════════════════════════════════════════════════╝

========== PRUEBA 1: Health Check =========
✓ API está activa y funcionando

[...]

========== RESUMEN DE PRUEBAS ==========
✓ Health Check
✓ Información
✓ Ejemplo de datos
✓ Predicción - Riesgo Bajo
✓ Predicción - Riesgo Alto
✓ Predicciones en Lote
✓ Validación de Errores

Total: 7/7 pruebas exitosas
¡Todas las pruebas pasaron correctamente!
```

## Ejemplos de Uso

### Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# Datos del paciente
datos = {
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
}

# Hacer predicción
response = requests.post(f"{BASE_URL}/predecir", json=datos)
resultado = response.json()

print(f"Riesgo: {resultado['health_risk'].upper()}")
print(f"Confianza: {resultado['confidence']*100:.1f}%")
print(f"Interpretación: {resultado['risk_level']}")
```

### JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000";

const datos = {
    age: 45,
    weight: 75,
    height: 175,
    sleep: 7.5,
    bmi: 24.5,
    exercise: "medium",
    sugar_intake: "medium",
    smoking: "no",
    alcohol: "no",
    married: "yes",
    profession: "office_worker"
};

fetch(`${BASE_URL}/predecir`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos)
})
.then(res => res.json())
.then(data => {
    console.log(`Riesgo: ${data.health_risk.toUpperCase()}`);
    console.log(`Confianza: ${(data.confidence * 100).toFixed(1)}%`);
    console.log(`Interpretación: ${data.risk_level}`);
});
```

### cURL

```bash
# Predicción individual
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

# Health check
curl http://localhost:8000/health

# Obtener ejemplo
curl http://localhost:8000/ejemplo
```

## Estructura del Código

```
api/
├── main.py          # Aplicación FastAPI principal
├── test_api.py      # Script de pruebas automatizadas
└── README.md        # Esta documentación
```

## Modelo Utilizado

- **Modelo**: `sk_auto_best_tuned.joblib`
- **Algoritmo**: XGBoost (entrenado con AutoML)
- **Características**: 11 variables de entrada
- **Target**: Riesgo de salud (high/low)
- **Precisión en test**: ~82%
- **AUC-ROC**: ~0.92

## Solución de Problemas

### Error: "No se puede conectar a localhost:8000"

**Solución:** Asegúrate de que la API está corriendo:
```bash
cd api
python main.py
```

### Error: "El modelo no está cargado correctamente"

**Solución:** Verifica que el archivo `models/sk_auto_best_tuned.joblib` existe:
```bash
ls -lh ../models/sk_auto_best_tuned.joblib
```

### Error de validación: "Age out of range"

**Solución:** Usa valores dentro de los rangos válidos:
- age: 18-100
- weight: 30-200
- height: 100-250
- sleep: 0-24
- bmi: 10-60

### Puerto 8000 en uso

**Solución:** Usa otro puerto:
```bash
python main.py --port 8080
# O
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Desplegar a Producción

### Con Gunicorn (recomendado para producción)

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Con Docker

```bash
# Crear Dockerfile (si no existe)
docker build -t health-risk-api .
docker run -p 8000:8000 health-risk-api
```

## API Reference

Para ver la referencia completa de la API con todos los detalles de parámetros y respuestas, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Contacto y Soporte

Si encuentras problemas o tienes sugerencias, abre un issue en el repositorio del proyecto.

---

**Hecho con ❤️ usando FastAPI y Machine Learning**