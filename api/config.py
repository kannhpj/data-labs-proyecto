"""
Configuración de la API de predicción de riesgo de salud
"""

from pathlib import Path

# Rutas
PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "sk_auto_best_tuned.joblib"

# Configuración de la API
API_TITLE = "Predictor de Riesgo de Salud"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API para predecir el nivel de riesgo de salud basado en datos personales y de estilo de vida"

# Puerto por defecto
DEFAULT_PORT = 8000
DEFAULT_HOST = "0.0.0.0"

# Validaciones
AGE_MIN = 18
AGE_MAX = 100

WEIGHT_MIN = 30
WEIGHT_MAX = 200

HEIGHT_MIN = 100
HEIGHT_MAX = 250

SLEEP_MIN = 0
SLEEP_MAX = 24

BMI_MIN = 10
BMI_MAX = 60

# Valores válidos para campos categóricos
EXERCISE_OPTIONS = ["low", "medium", "high"]
SUGAR_INTAKE_OPTIONS = ["low", "medium", "high"]
SMOKING_OPTIONS = ["yes", "no"]
ALCOHOL_OPTIONS = ["yes", "no"]
MARRIED_OPTIONS = ["yes", "no"]
PROFESSION_OPTIONS = [
    "office_worker",
    "teacher",
    "artist",
    "student",
    "engineer",
    "doctor",
    "salesman",
    "nurse"
]

# Mensajes
MESSAGES = {
    "model_loaded": "✓ Modelo cargado exitosamente",
    "model_error": "✗ Error al cargar el modelo",
    "api_started": "✓ API iniciada correctamente",
    "prediction_success": "Predicción realizada exitosamente",
    "prediction_error": "Error en la predicción",
}