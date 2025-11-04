"""
Script de prueba para la API de predicción de riesgo de salud
Ejecuta: python test_api.py (cuando la API esté corriendo)
"""

import requests
import json
from typing import Dict, Any

# URL de la API
BASE_URL = "http://localhost:8000"

# Colores para salida en terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_section(title: str):
    """Imprimir título de sección"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"{title.center(60)}")
    print(f"{'='*60}{Colors.ENDC}\n")


def print_success(message: str):
    """Imprimir mensaje de éxito"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message: str):
    """Imprimir mensaje de error"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message: str):
    """Imprimir mensaje de información"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def print_response(response: Dict[Any, Any], title: str = "Respuesta"):
    """Imprimir respuesta formateada"""
    print(f"\n{Colors.BOLD}{title}:{Colors.ENDC}")
    print(json.dumps(response, indent=2, ensure_ascii=False))


def test_health_check():
    """Prueba 1: Verificar que la API está activa"""
    print_section("PRUEBA 1: Health Check")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("API está activa y funcionando")
            data = response.json()
            print_response(data, "Estado del servidor")
            return True
        else:
            print_error(f"Error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"No se puede conectar a {BASE_URL}")
        print_info("¿La API está corriendo? Ejecuta: python api/main.py")
        return False
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return False


def test_root():
    """Prueba 2: Obtener información de la API"""
    print_section("PRUEBA 2: Información de la API")

    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        data = response.json()
        print_response(data, "Información disponible")
        return True
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_ejemplo():
    """Prueba 3: Obtener ejemplo de datos"""
    print_section("PRUEBA 3: Datos de Ejemplo")

    try:
        response = requests.get(f"{BASE_URL}/ejemplo", timeout=5)
        data = response.json()
        print_response(data, "Datos de ejemplo")
        return True
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_prediccion_riesgo_bajo():
    """Prueba 4: Predicción con riesgo probablemente BAJO"""
    print_section("PRUEBA 4: Predicción de Riesgo Bajo")

    # Datos de persona joven, activa, con buenos hábitos
    datos = {
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

    print(f"{Colors.BOLD}Datos del paciente:{Colors.ENDC}")
    for key, value in datos.items():
        print(f"  • {key}: {value}")

    try:
        response = requests.post(f"{BASE_URL}/predecir", json=datos, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print_success("Predicción realizada")
            print_response(result, "Resultado")

            # Destacar el resultado
            risk = result.get("health_risk", "desconocido").upper()
            confidence = result.get("confidence", 0) * 100
            print(f"\n{Colors.BOLD}Resumen:{Colors.ENDC}")
            print(f"  Riesgo: {Colors.OKGREEN if risk == 'LOW' else Colors.FAIL}{risk}{Colors.ENDC}")
            print(f"  Confianza: {confidence:.1f}%")
            return True
        else:
            print_error(f"Error: {response.status_code}")
            print_response(response.json(), "Detalle del error")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_prediccion_riesgo_alto():
    """Prueba 5: Predicción con riesgo probablemente ALTO"""
    print_section("PRUEBA 5: Predicción de Riesgo Alto")

    # Datos de persona mayor, sedentaria, con hábitos no saludables
    datos = {
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

    print(f"{Colors.BOLD}Datos del paciente:{Colors.ENDC}")
    for key, value in datos.items():
        print(f"  • {key}: {value}")

    try:
        response = requests.post(f"{BASE_URL}/predecir", json=datos, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print_success("Predicción realizada")
            print_response(result, "Resultado")

            # Destacar el resultado
            risk = result.get("health_risk", "desconocido").upper()
            confidence = result.get("confidence", 0) * 100
            print(f"\n{Colors.BOLD}Resumen:{Colors.ENDC}")
            print(f"  Riesgo: {Colors.OKGREEN if risk == 'LOW' else Colors.FAIL}{risk}{Colors.ENDC}")
            print(f"  Confianza: {confidence:.1f}%")
            return True
        else:
            print_error(f"Error: {response.status_code}")
            print_response(response.json(), "Detalle del error")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_prediccion_multiple():
    """Prueba 6: Predicciones para múltiples pacientes"""
    print_section("PRUEBA 6: Predicciones en Lote (Batch)")

    datos_lista = [
        {
            "age": 25,
            "weight": 70,
            "height": 180,
            "sleep": 8.0,
            "bmi": 21.6,
            "exercise": "high",
            "sugar_intake": "low",
            "smoking": "no",
            "alcohol": "no",
            "married": "no",
            "profession": "student"
        },
        {
            "age": 50,
            "weight": 85,
            "height": 172,
            "sleep": 6.5,
            "bmi": 28.7,
            "exercise": "medium",
            "sugar_intake": "medium",
            "smoking": "no",
            "alcohol": "yes",
            "married": "yes",
            "profession": "teacher"
        },
        {
            "age": 70,
            "weight": 75,
            "height": 165,
            "sleep": 7.0,
            "bmi": 27.5,
            "exercise": "low",
            "sugar_intake": "high",
            "smoking": "yes",
            "alcohol": "no",
            "married": "yes",
            "profession": "doctor"
        }
    ]

    print(f"{Colors.BOLD}Prediciendo para {len(datos_lista)} pacientes...{Colors.ENDC}\n")

    try:
        response = requests.post(f"{BASE_URL}/predecir-batch", json=datos_lista, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print_success(f"Predicciones completadas")

            total = result.get("total_predicciones", 0)
            print(f"\n{Colors.BOLD}Total de predicciones: {total}{Colors.ENDC}\n")

            for i, pred in enumerate(result.get("predicciones", []), 1):
                risk = pred.get("health_risk", "?").upper()
                confidence = pred.get("confidence", 0) * 100
                color = Colors.OKGREEN if risk == "LOW" else Colors.FAIL
                print(f"Paciente {i}: {color}{risk}{Colors.ENDC} (confianza: {confidence:.1f}%)")

            return True
        else:
            print_error(f"Error: {response.status_code}")
            print_response(response.json(), "Detalle del error")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_validacion_errores():
    """Prueba 7: Validación de errores con datos inválidos"""
    print_section("PRUEBA 7: Validación de Errores")

    datos_invalidos = {
        "age": 150,  # Edad fuera de rango
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

    print(f"{Colors.BOLD}Intentando con datos inválidos:{Colors.ENDC}")
    print(f"  • age: 150 (rango válido: 18-100)")

    try:
        response = requests.post(f"{BASE_URL}/predecir", json=datos_invalidos, timeout=5)
        if response.status_code != 200:
            print_success("Sistema rechazó correctamente los datos inválidos")
            print_response(response.json(), "Mensaje de error")
            return True
        else:
            print_error("Sistema no validó correctamente los datos")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def main():
    """Ejecutar todas las pruebas"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔" + "=" * 58 + "╗")
    print("║" + "PRUEBAS DE LA API DE PREDICCIÓN DE RIESGO DE SALUD".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print(f"{Colors.ENDC}")

    pruebas = [
        ("Health Check", test_health_check),
        ("Información", test_root),
        ("Ejemplo de datos", test_ejemplo),
        ("Predicción - Riesgo Bajo", test_prediccion_riesgo_bajo),
        ("Predicción - Riesgo Alto", test_prediccion_riesgo_alto),
        ("Predicciones en Lote", test_prediccion_multiple),
        ("Validación de Errores", test_validacion_errores),
    ]

    resultados = []
    for nombre, test_func in pruebas:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Pruebas interrumpidas por el usuario{Colors.ENDC}")
            break
        except Exception as e:
            print_error(f"Error inesperado en {nombre}: {e}")
            resultados.append((nombre, False))

    # Resumen final
    print_section("RESUMEN DE PRUEBAS")
    exitosas = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)

    print(f"{Colors.BOLD}Resultados:{Colors.ENDC}")
    for nombre, resultado in resultados:
        símbolo = Colors.OKGREEN + "✓" + Colors.ENDC if resultado else Colors.FAIL + "✗" + Colors.ENDC
        print(f"  {símbolo} {nombre}")

    print(f"\n{Colors.BOLD}Total: {exitosas}/{total} pruebas exitosas{Colors.ENDC}\n")

    if exitosas == total:
        print(f"{Colors.OKGREEN}¡Todas las pruebas pasaron correctamente!{Colors.ENDC}\n")
    else:
        print(f"{Colors.WARNING}Algunas pruebas fallaron. Revisa los mensajes arriba.{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Programa interrumpido{Colors.ENDC}\n")
    except Exception as e:
        print_error(f"Error fatal: {e}")