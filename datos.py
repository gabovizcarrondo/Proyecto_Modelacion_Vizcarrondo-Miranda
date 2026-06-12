"""
Datos base del enunciado: configuracion de la zona, pesos y establecimientos.
Estos valores son el punto de partida; el usuario puede modificarlos desde el menu.
"""

CONFIGURACION_BASE = {
    "calle_min": 50,
    "calle_max": 55,
    "carrera_min": 10,
    "carrera_max": 15,
    "peso_base": 5,
    "calles_especiales": {51: 10},
    "carreras_especiales": {11: 7, 12: 7, 13: 7},
    "javier": (54, 14),
    "andreina": (52, 13),
}

ESTABLECIMIENTOS = [
    {"nombre": "Discoteca The Darkness", "calle": 50, "carrera": 14},
    {"nombre": "Bar La Pasión", "calle": 54, "carrera": 11},
    {"nombre": "Cervecería Mi Rolita", "calle": 50, "carrera": 12},
]

DESTINO_CASO_BASE = {
    "nombre": "Discoteca The Darkness",
    "ubicacion": (50, 14),
}
