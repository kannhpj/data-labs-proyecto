"""
API FastAPI para predicción de riesgo de salud
Utiliza el mejor modelo entrenado (sk_auto_best_tuned.joblib)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import uvicorn

# Crear aplicación FastAPI
app = FastAPI(
    title="Predictor de Riesgo de Salud",
    description="API para predecir el nivel de riesgo de salud basado en datos personales y de estilo de vida",
    version="1.0.0"
)

# Configurar CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

# Cargar el modelo entrenado
MODEL_PATH = Path(__file__).parent.parent / "models" / "sk_auto_best_tuned.joblib"

try:
    model_data = joblib.load(MODEL_PATH)
    pipeline = model_data["pipeline"]
    label_encoder = model_data["label_encoder"]
    print(f"✓ Modelo cargado exitosamente desde: {MODEL_PATH}")
except Exception as e:
    print(f"✗ Error al cargar el modelo: {e}")
    pipeline = None
    label_encoder = None


# Definir esquema de entrada con Pydantic
class HealthData(BaseModel):
    """Esquema para los datos de salud del paciente"""

    age: int = Field(..., ge=18, le=100, description="Edad del paciente (18-100)")
    weight: int = Field(..., ge=30, le=200, description="Peso en kg (30-200)")
    height: int = Field(..., ge=100, le=250, description="Altura en cm (100-250)")
    sleep: float = Field(..., ge=0, le=24, description="Horas de sueño diarias (0-24)")
    bmi: float = Field(..., ge=10, le=60, description="Índice de masa corporal (10-60)")
    exercise: str = Field(..., description="Nivel de ejercicio: 'low', 'medium', 'high'")
    sugar_intake: Optional[str] = Field(default="medium", description="Consumo de azúcar: 'low', 'medium', 'high'")
    smoking: str = Field(..., description="¿Fuma? 'yes' o 'no'")
    alcohol: str = Field(..., description="¿Consume alcohol? 'yes' o 'no'")
    married: str = Field(..., description="¿Estado civil? 'yes' (casado/a) o 'no'")
    profession: str = Field(..., description="Profesión: 'office_worker', 'teacher', 'artist', 'student', 'engineer', 'doctor', 'salesman', 'nurse'")

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class PredictionResponse(BaseModel):
    """Esquema para la respuesta de predicción"""

    health_risk: str = Field(..., description="Nivel de riesgo predicho: 'high' o 'low'")
    confidence: float = Field(..., ge=0, le=1, description="Confianza de la predicción (0-1)")
    risk_level: str = Field(..., description="Interpretación del riesgo: 'Alto' o 'Bajo'")


@app.get("/", tags=["info"])
def root():
    """Endpoint raíz con información de la API"""
    return {
        "nombre": "Predictor de Riesgo de Salud",
        "versión": "1.0.0",
        "descripción": "API para predecir el nivel de riesgo de salud",
        "endpoints": {
            "info": "GET /",
            "documentación": "GET /docs",
            "predicción": "POST /predecir",
            "ejemplo": "GET /ejemplo"
        }
    }


@app.get("/ejemplo", tags=["info"])
def ejemplo():
    """Retorna un ejemplo de datos para hacer una predicción"""
    return {
        "ejemplo_entrada": {
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
        },
        "descripción": "Usa estos datos en el endpoint POST /predecir",
        "valores_validos": {
            "exercise": ["low", "medium", "high"],
            "sugar_intake": ["low", "medium", "high"],
            "smoking": ["yes", "no"],
            "alcohol": ["yes", "no"],
            "married": ["yes", "no"],
            "profession": ["office_worker", "teacher", "artist", "student", "engineer", "doctor", "salesman", "nurse"]
        }
    }


@app.post("/predecir", response_model=PredictionResponse, tags=["predicciones"])
def predecir(datos: HealthData):
    """
    Hacer una predicción de riesgo de salud

    Envía los datos del paciente y recibe la predicción del modelo.
    """

    if pipeline is None or label_encoder is None:
        raise HTTPException(status_code=500, detail="El modelo no está cargado correctamente")

    try:
        # Preparar los datos en el formato esperado por el modelo
        df_input = pd.DataFrame([{
            'age': datos.age,
            'weight': datos.weight,
            'height': datos.height,
            'exercise': datos.exercise.lower(),
            'sleep': datos.sleep,
            'sugar_intake': datos.sugar_intake.lower() if datos.sugar_intake else 'medium',
            'smoking': datos.smoking.lower(),
            'alcohol': datos.alcohol.lower(),
            'married': datos.married.lower(),
            'profession': datos.profession.lower(),
            'bmi': datos.bmi
        }])

        # Hacer la predicción
        prediction = pipeline.predict(df_input)[0]
        probabilities = pipeline.predict_proba(df_input)[0]

        # Decodificar la predicción
        risk_prediction = label_encoder.inverse_transform([prediction])[0]

        # Obtener la confianza (probabilidad máxima)
        confidence = float(np.max(probabilities))

        # Interpretar el riesgo
        risk_interpretation = "Alto - Recomendamos consultar a un médico" if risk_prediction == "high" else "Bajo - Mantener estilos de vida saludables"

        return PredictionResponse(
            health_risk=risk_prediction,
            confidence=confidence,
            risk_level=risk_interpretation
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {str(e)}")


@app.post("/predecir-batch", tags=["predicciones"])
def predecir_batch(datos_lista: list[HealthData]):
    """
    Hacer predicciones para múltiples pacientes

    Envía una lista de pacientes y recibe predicciones para todos.
    """

    if pipeline is None or label_encoder is None:
        raise HTTPException(status_code=500, detail="El modelo no está cargado correctamente")

    try:
        # Convertir lista de objetos a DataFrame
        data_dicts = []
        for datos in datos_lista:
            data_dicts.append({
                'age': datos.age,
                'weight': datos.weight,
                'height': datos.height,
                'exercise': datos.exercise.lower(),
                'sleep': datos.sleep,
                'sugar_intake': datos.sugar_intake.lower() if datos.sugar_intake else 'medium',
                'smoking': datos.smoking.lower(),
                'alcohol': datos.alcohol.lower(),
                'married': datos.married.lower(),
                'profession': datos.profession.lower(),
                'bmi': datos.bmi
            })

        df_input = pd.DataFrame(data_dicts)

        # Hacer predicciones
        predictions = pipeline.predict(df_input)
        probabilities = pipeline.predict_proba(df_input)

        # Decodificar y formatear respuestas
        resultados = []
        for pred, probs in zip(predictions, probabilities):
            risk = label_encoder.inverse_transform([pred])[0]
            confidence = float(np.max(probs))
            risk_interpretation = "Alto - Recomendamos consultar a un médico" if risk == "high" else "Bajo - Mantener estilos de vida saludables"

            resultados.append({
                "health_risk": risk,
                "confidence": confidence,
                "risk_level": risk_interpretation
            })

        return {
            "total_predicciones": len(resultados),
            "predicciones": resultados
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en las predicciones: {str(e)}")


@app.get("/health", tags=["info"])
def health_check():
    """Verificar que la API está funcionando"""
    return {
        "estado": "OK",
        "modelo_cargado": pipeline is not None,
        "encoder_cargado": label_encoder is not None
    }


if __name__ == "__main__":
    # Ejecutar con: python main.py
    # O con: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)