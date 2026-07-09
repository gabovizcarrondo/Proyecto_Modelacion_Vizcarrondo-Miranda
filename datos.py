"""
Datos base del enunciado: configuracion de la zona, pesos y establecimientos.

Los valores se cargan desde config.json en tiempo de ejecucion.
El usuario puede modificarlos adicionalmente desde el menu de consola.
"""

import json
import os


def _ruta_config():
    """Ruta de config.json relativa a la ubicacion de este modulo."""
    return os.path.join(os.path.dirname(__file__), "config.json")


def _cargar_config():
    """Lee y parsea config.json desde disco."""
    with open(_ruta_config(), encoding="utf-8") as archivo:
        return json.load(archivo)


def _convertir_configuracion_base(datos):
    """
    Convierte el JSON a la estructura esperada por el resto del proyecto.

    - javier/andreina: listas JSON -> tuplas
    - calles_especiales/carreras_especiales: claves str -> int
    """
    return {
        "calle_min": datos["calle_min"],
        "calle_max": datos["calle_max"],
        "carrera_min": datos["carrera_min"],
        "carrera_max": datos["carrera_max"],
        "peso_base": datos["peso_base"],
        "calles_especiales": {
            int(calle): minutos for calle, minutos in datos["calles_especiales"].items()
        },
        "carreras_especiales": {
            int(carrera): minutos
            for carrera, minutos in datos["carreras_especiales"].items()
        },
        "javier": tuple(datos["javier"]),
        "andreina": tuple(datos["andreina"]),
    }


def _convertir_establecimientos(datos):
    """Convierte la lista de establecimientos del JSON."""
    return [dict(establecimiento) for establecimiento in datos["establecimientos"]]


def _convertir_destino_caso_base(datos):
    """Convierte el destino del caso base del JSON."""
    destino = datos["destino_caso_base"]
    return {
        "nombre": destino["nombre"],
        "ubicacion": (destino["calle"], destino["carrera"]),
    }


_config = _cargar_config()

CONFIGURACION_BASE = _convertir_configuracion_base(_config)
ESTABLECIMIENTOS = _convertir_establecimientos(_config)
DESTINO_CASO_BASE = _convertir_destino_caso_base(_config)
