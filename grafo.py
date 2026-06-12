"""
Construccion y validacion del grafo como lista de adyacencia.

Convencion del mapa segun el enunciado:
- Las calles crecen hacia el norte.
- Las carreras crecen desde el este hacia el oeste.
"""


def reglas_desde_configuracion(configuracion):
    """Extrae las reglas de peso a partir de la configuracion activa."""
    return {
        "peso_base": configuracion["peso_base"],
        "calles_especiales": configuracion["calles_especiales"],
        "carreras_especiales": configuracion["carreras_especiales"],
    }


def crear_grafo(calle_min, calle_max, carrera_min, carrera_max, reglas_peso):
    """
    Construye el grafo como lista de adyacencia.

    Retorna un diccionario {nodo: [(vecino, peso), ...]} donde cada nodo
    es una tupla (calle, carrera).
    """
    grafo = {}

    for calle in range(calle_min, calle_max + 1):
        for carrera in range(carrera_min, carrera_max + 1):
            grafo[(calle, carrera)] = []

    for calle in range(calle_min, calle_max + 1):
        for carrera in range(carrera_min, carrera_max + 1):
            nodo = (calle, carrera)

            # Vecino con carrera mayor (hacia el oeste; las carreras crecen de este a oeste)
            if carrera < carrera_max:
                vecino = (calle, carrera + 1)
                peso = obtener_peso_arista(nodo, vecino, reglas_peso)
                grafo[nodo].append((vecino, peso))
                grafo[vecino].append((nodo, peso))

            # Vecino con calle mayor (hacia el norte; las calles crecen hacia el norte)
            if calle < calle_max:
                vecino = (calle + 1, carrera)
                peso = obtener_peso_arista(nodo, vecino, reglas_peso)
                grafo[nodo].append((vecino, peso))
                grafo[vecino].append((nodo, peso))

    return grafo


def obtener_peso_arista(nodo_origen, nodo_destino, reglas_peso):
    """
    Calcula el tiempo en minutos de recorrer una cuadra entre dos nodos vecinos.

    Interpretacion del desplazamiento segun el enunciado:
    - Si el movimiento mantiene la misma calle y cambia la carrera, la persona
      esta caminando sobre esa calle (desplazamiento horizontal en el mapa).
      Por eso el peso depende de la calle por la que se transita.
    - Si el movimiento mantiene la misma carrera y cambia la calle, la persona
      esta caminando sobre esa carrera (desplazamiento vertical en el mapa).
      Por eso el peso depende de la carrera por la que se transita.
    """
    calle_o, carrera_o = nodo_origen
    calle_d, carrera_d = nodo_destino

    peso_base = reglas_peso.get("peso_base", 5)
    calles_especiales = reglas_peso.get("calles_especiales", {})
    carreras_especiales = reglas_peso.get("carreras_especiales", {})

    # Misma calle, carrera distinta: se camina sobre la calle
    if calle_o == calle_d and carrera_o != carrera_d:
        return calles_especiales.get(calle_o, peso_base)

    # Misma carrera, calle distinta: se camina sobre la carrera
    if carrera_o == carrera_d and calle_o != calle_d:
        return carreras_especiales.get(carrera_o, peso_base)

    return peso_base


def obtener_vecinos(grafo, nodo):
    """Retorna la lista de nodos vecinos conectados a un nodo dado."""
    return [vecino for vecino, _ in grafo.get(nodo, [])]


def validar_ubicacion(ubicacion, configuracion, nombre="Ubicacion"):
    """
    Verifica que una ubicacion este dentro de los limites de la zona.

    Acepta una tupla (calle, carrera) o un diccionario con claves calle y carrera.
    """
    if isinstance(ubicacion, dict):
        calle = ubicacion["calle"]
        carrera = ubicacion["carrera"]
        etiqueta = ubicacion.get("nombre", nombre)
    else:
        calle, carrera = ubicacion
        etiqueta = nombre

    dentro = (
        configuracion["calle_min"] <= calle <= configuracion["calle_max"]
        and configuracion["carrera_min"] <= carrera <= configuracion["carrera_max"]
    )

    if not dentro:
        raise ValueError(
            f"La ubicacion de {etiqueta} ({calle}, {carrera}) esta fuera de la zona "
            f"(Calles {configuracion['calle_min']}-{configuracion['calle_max']}, "
            f"Carreras {configuracion['carrera_min']}-{configuracion['carrera_max']})."
        )
