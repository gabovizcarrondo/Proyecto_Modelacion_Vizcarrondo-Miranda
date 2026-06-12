"""
Utilidades generales: copia de configuracion, lectura por consola y formato.
"""

from datos import CONFIGURACION_BASE


def copiar_configuracion():
    """Crea una copia independiente de la configuracion base para no alterarla."""
    return {
        "calle_min": CONFIGURACION_BASE["calle_min"],
        "calle_max": CONFIGURACION_BASE["calle_max"],
        "carrera_min": CONFIGURACION_BASE["carrera_min"],
        "carrera_max": CONFIGURACION_BASE["carrera_max"],
        "peso_base": CONFIGURACION_BASE["peso_base"],
        "calles_especiales": dict(CONFIGURACION_BASE["calles_especiales"]),
        "carreras_especiales": dict(CONFIGURACION_BASE["carreras_especiales"]),
        "javier": CONFIGURACION_BASE["javier"],
        "andreina": CONFIGURACION_BASE["andreina"],
    }


def leer_entero(mensaje, valor_defecto=None, permitir_vacio=False):
    """Lee un entero; si hay valor por defecto y el usuario presiona Enter, lo usa."""
    if valor_defecto is not None:
        prompt = f"{mensaje} [{valor_defecto}]: "
    else:
        prompt = f"{mensaje}: "

    while True:
        entrada = input(prompt).strip()
        if entrada == "" and valor_defecto is not None:
            return valor_defecto
        if entrada == "" and permitir_vacio:
            return None
        try:
            return int(entrada)
        except ValueError:
            print("  Entrada invalida. Ingrese un numero entero.")


def leer_texto(mensaje, valor_defecto=None):
    """Lee texto desde consola."""
    if valor_defecto is not None:
        prompt = f"{mensaje} [{valor_defecto}]: "
    else:
        prompt = f"{mensaje}: "

    entrada = input(prompt).strip()
    if entrada == "" and valor_defecto is not None:
        return valor_defecto
    return entrada


def normalizar_destino(destino):
    """
    Unifica un destino al formato con calle y carrera.

    Acepta destinos con clave 'ubicacion' como tupla (calle, carrera)
    o con claves 'calle' y 'carrera' directamente.
    """
    destino_normalizado = dict(destino)
    if "ubicacion" in destino_normalizado:
        calle, carrera = destino_normalizado["ubicacion"]
        destino_normalizado["calle"] = calle
        destino_normalizado["carrera"] = carrera
    return destino_normalizado


def formatear_ruta(camino):
    """Convierte la lista de nodos en una cadena legible."""
    if not camino:
        return "Sin ruta disponible"
    partes = [f"Calle {calle} con Carrera {carrera}" for calle, carrera in camino]
    return " -> ".join(partes)


def pausar():
    """Pausa breve para que el usuario lea el resultado antes de volver al menu."""
    input("\nPresione Enter para continuar...")
