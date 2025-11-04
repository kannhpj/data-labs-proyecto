# Predictor de Riesgo de Salud

Un proyecto de machine learning que predice el nivel de riesgo de salud (alto/bajo) basado en datos de estilo de vida y caracteristicas de salud usando AutoML.

## Que hace?

Analiza datos de pacientes como edad, peso, altura, ejercicio, sueno, consumo de azucar, fumar, alcohol, estado civil y profesion para predecir si tienen riesgo alto o bajo de problemas de salud.

## Requisitos previos

- Python 3.13 o superior
- Git
- pip (gestor de paquetes de Python)

## Instalacion (pasos rapidos)

### 1. Clonar el repositorio
```bash
git clone https://github.com/kannhpj/data-labs-proyecto.git
cd data-labs-proyecto
```

### 2. Crear ambiente virtual
```bash
python -m venv .venv
```

### 3. Activar ambiente virtual


**En Linux/Mac:**
```bash
source .venv/bin/activate
```

**En Windows:**
```bash
.venv\Scripts\activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Ejecucion

### Ver los analisis (Notebooks)

Una vez instalado, ejecuta Jupyter:

```bash
jupyter notebook
```

Se abrir en tu navegador. Navega a la carpeta `notebooks/` y abre los archivos en este orden:

1. **`01_datos.ipynb`** - Carga y primeras exploraciones de datos
2. **`02_Exploracion_datos.ipynb`** - Analisis profundo de los datos (m�s importante)
3. **`02_Analisis con Ydata.ipynb`** - Analisis de calidad de datos
4. **`03_AutoML_PyCaret.ipynb`** - Entrenamiento automatico del modelo

### Ver el reporte final

El reporte HTML interactivo con todos los resultados y graficos:

```bash
# Opcion 1: Abrir directamente en el navegador (Linux/Mac)
open notebooks/Informe_Final_Salud.html

# Opcio 2: Ejecutar servidor web local
python -m http.server 8000 --directory ./notebooks

# Luego abre en el navegador:
# http://localhost:8000/Informe_Final_Salud.html
```

### Usar la API para hacer predicciones

El proyecto incluye una **API FastAPI** lista para usar:

```bash
# Ir a la carpeta de la API
cd api

# Ejecutar la API
python main.py
```

Luego accede a:
- **Documentacion interactiva**: http://localhost:8000/docs
- **Realizar predicciones**: POST a http://localhost:8000/predecir

Para más detalles, consulta: [QUICK_START_API.md](QUICK_START_API.md) o [api/README.md](api/README.md)

**Ejemplo de prediccion:**
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


## Estructura del Proyecto

data-labs-proyecto/
├── .venv/ # Entorno virtual de Python para aislar dependencias del proyecto
├── api/ # API FastAPI para hacer predicciones
│ ├── main.py # Aplicación FastAPI principal
│ ├── test_api.py # Script de pruebas automatizadas de la API
│ ├── config.py # Configuración general de la API
│ ├── requirements_api.txt # Dependencias mínimas para la API
│ └── README.md # Documentación detallada de la API
├── datos/ # Carpeta para los datos fuente y generados
├── models/ # Modelos de Machine Learning entrenados y configuraciones
├── notebooks/ # Jupyter Notebooks para análisis y experimentación interactiva
│ ├── 01_datos.ipynb # Exploración inicial de los datos
│ ├── 02_Exploracion_datos.ipynb # Análisis exploratorio (parte 1)
│ ├── 02_Exploracion_datos2.ipynb # Análisis exploratorio (parte 2)
│ ├── 03_AutoML_PyCaret.ipynb # Experimentos de AutoML con PyCaret
│ └── Informe_Final_Salud.html # Informe final exportado en HTML
├── logs.log # Registro de eventos y errores del proyecto
├── .gitignore # Exclusiones para control de versiones con Git
├── .python-version # Versión de Python recomendada para el proyecto
├── main.py # Script principal para la lógica central del proyecto
├── pyproject.toml # Configuración de dependencias y herramientas Python
├── README.md # Documentación principal del proyecto
├── QUICK_START_API.md # Guía rápida de inicio para la API
└── requirements.txt # Lista de dependencias Python del entorno principal



## Dependencias principales

- **pandas, numpy** - Procesamiento de datos
- **scikit-learn** - Machine learning
- **pycaret** - AutoML (entrenamiento automatico)
- **matplotlib, seaborn, plotly** - Visualizaciones
- **jupyter** - Notebooks interactivos
- **xgboost, lightgbm** - Modelos avanzados

## Flujo de trabajo

1. **Carga de datos** : `01_datos.ipynb`
2. **Exploracion y analisis** : `02_Exploracion_datos.ipynb`
3. **Analisis de calidad** : `02_Analisis con Ydata.ipynb`
4. **Entrenar modelo AutoML** : `03_AutoML_PyCaret.ipynb`
5. **Ver resultados** : `Informe_Final_Salud.html`

## Modelos entrenados

El proyecto ya incluye modelos pre-entrenados en la carpeta `models/`:
- `sk_auto_best.joblib` - Mejor modelo
- `sk_auto_best_tuned.joblib` - Modelo fine-tuned

Puedes usarlos para hacer predicciones sin volver a entrenar.

## Comandos utiles

```bash
# Verificar version de Python
python --version

# Listar dependencias instaladas
pip list

# Desactivar ambiente virtual
deactivate

# Ejecutar solo main.py
python main.py
```

## Autores

- Edgar Fernando Estrada Arteaga 

- Juan Manuel Sierra Arcila

- Juan Diego Castaño Ceballos


## Licencia

MIT

---

