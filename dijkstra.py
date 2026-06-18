"""
Algoritmo de Dijkstra implementado manualmente (sin librerias externas).

Incluye adaptacion para evitar que dos personas compartan el mismo tramo
(arista) de calle/carrera al mismo tiempo.

Interpretacion conservadora de la restriccion de privacidad:
para garantizar que Javier y Andreina no sean vistos caminando juntos,
se evita que ambas rutas compartan tramos (aristas) de calle o carrera.
Compartir una interseccion en momentos distintos si se permite; lo prohibido es usar el mismo tramo.
"""

# Cambiar a True para imprimir aristas de debug en consola al calcular rutas.
DEBUG_PRIVACIDAD = False


def arista_canonica(nodo_a, nodo_b):
    """
    Representa una arista no dirigida con forma canonica unica.

    Ejemplo: ((52, 13), (52, 14)) es igual a ((52, 14), (52, 13)).
    """
    return tuple(sorted([tuple(nodo_a), tuple(nodo_b)]))


def obtener_aristas_de_ruta(ruta):
    """
    Convierte una lista de nodos en el conjunto de aristas no dirigidas que recorre.
    """
    aristas = set()
    for i in range(len(ruta) - 1):
        aristas.add(arista_canonica(ruta[i], ruta[i + 1]))
    return aristas


def obtener_aristas_compartidas(ruta1, ruta2):
    """Devuelve las aristas que ambas rutas tienen en comun."""
    return obtener_aristas_de_ruta(ruta1) & obtener_aristas_de_ruta(ruta2)


def rutas_comparten_tramos(ruta1, ruta2):
    """
    Indica si dos rutas usan al menos un mismo tramo (arista).

    Compartir una interseccion (nodo) no cuenta como compartir tramo.
    """
    if not ruta1 or not ruta2:
        return False
    return bool(obtener_aristas_compartidas(ruta1, ruta2))


def imprimir_debug_aristas(ruta_javier, ruta_andreina):
    """Muestra en consola las aristas de cada ruta y las compartidas (solo debug)."""
    aristas_javier = obtener_aristas_de_ruta(ruta_javier)
    aristas_andreina = obtener_aristas_de_ruta(ruta_andreina)
    compartidas = aristas_javier & aristas_andreina

    print("\n[Debug privacidad]")
    print(f"  Aristas Javier ({len(aristas_javier)}): {sorted(aristas_javier)}")
    print(f"  Aristas Andreina ({len(aristas_andreina)}): {sorted(aristas_andreina)}")
    print(f"  Aristas compartidas ({len(compartidas)}): {sorted(compartidas)}")


def dijkstra(grafo, origen, destino, aristas_bloqueadas=None):
    """
    Encuentra la distancia minima desde origen hasta destino.

    Si se proporciona aristas_bloqueadas, Dijkstra ignora esas aristas.
    """
    if aristas_bloqueadas is None:
        aristas_bloqueadas = set()

    origen = tuple(origen)
    destino = tuple(destino)

    distancias = {nodo: float("inf") for nodo in grafo}
    distancias[origen] = 0
    predecesores = {nodo: None for nodo in grafo}
    visitados = set()
    pendientes = [(0, origen)]

    while pendientes:
        indice_min = 0
        for i in range(1, len(pendientes)):
            if pendientes[i][0] < pendientes[indice_min][0]:
                indice_min = i
        distancia_actual, nodo_actual = pendientes.pop(indice_min)

        if nodo_actual in visitados:
            continue

        visitados.add(nodo_actual)

        if nodo_actual == destino:
            break

        for vecino, peso in grafo[nodo_actual]:
            if vecino in visitados:
                continue

            arista_actual = arista_canonica(nodo_actual, vecino)
            if arista_actual in aristas_bloqueadas:
                continue

            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = nodo_actual
                pendientes.append((nueva_distancia, vecino))

    distancia_destino = distancias.get(destino, float("inf"))
    if distancia_destino == float("inf"):
        return None, predecesores

    return distancia_destino, predecesores


def reconstruir_camino(predecesores, origen, destino):
    """Reconstruye el camino optimo desde el origen hasta el destino."""
    origen = tuple(origen)
    destino = tuple(destino)

    camino = []
    nodo_actual = destino

    while nodo_actual is not None:
        camino.append(nodo_actual)
        if nodo_actual == origen:
            break
        nodo_actual = predecesores.get(nodo_actual)

    if not camino or camino[-1] != origen:
        return []

    camino.reverse()
    return camino


def calcular_ruta(grafo, origen, destino, aristas_bloqueadas=None):
    """
    Calcula la ruta minima entre dos nodos.

    Retorna (tiempo_total, camino).
    """
    tiempo, predecesores = dijkstra(grafo, origen, destino, aristas_bloqueadas)
    camino = reconstruir_camino(predecesores, origen, destino)
    return tiempo, camino


def _calcular_sincronizacion(tiempo_javier, tiempo_andreina):
    """Determina quien debe salir antes segun los tiempos finales."""
    if tiempo_javier is None or tiempo_andreina is None:
        return None, None
    if tiempo_javier > tiempo_andreina:
        return "Javier", tiempo_javier - tiempo_andreina
    if tiempo_andreina > tiempo_javier:
        return "Andreina", tiempo_andreina - tiempo_javier
    return "Ambos", 0


def _alternativa_valida(camino_javier, camino_andreina, tiempo_javier, tiempo_andreina):
    """
    Verifica que una alternativa tenga rutas completas y sin tramos compartidos.
    """
    if tiempo_javier is None or tiempo_andreina is None:
        return False
    if not camino_javier or not camino_andreina:
        return False
    return not rutas_comparten_tramos(camino_javier, camino_andreina)


def calcular_rutas_pareja(grafo, ubicacion_javier, ubicacion_andreina, destino):
    """
    Calcula rutas para Javier y Andreina respetando la restriccion del enunciado:
    no pueden ser vistos caminando juntos, por lo que no comparten tramos.

    Se usa una interpretacion conservadora: bloquear aristas compartidas entre
    ambas rutas garantiza que no transiten el mismo tramo de calle/carrera
    al mismo tiempo, aunque podrian coincidir en una interseccion en distintos
    momentos.
    """
    ubicacion_javier = tuple(ubicacion_javier)
    ubicacion_andreina = tuple(ubicacion_andreina)
    destino = tuple(destino)

    tiempo_javier, camino_javier = calcular_ruta(grafo, ubicacion_javier, destino)
    tiempo_andreina, camino_andreina = calcular_ruta(grafo, ubicacion_andreina, destino)

    mensaje_restriccion = None
    rutas_ajustadas = False
    advertencia_final = None

    if tiempo_javier is None or tiempo_andreina is None:
        quien_sale_antes, minutos_antes = _calcular_sincronizacion(
            tiempo_javier, tiempo_andreina
        )
        return _resultado_rutas(
            camino_javier,
            tiempo_javier,
            camino_andreina,
            tiempo_andreina,
            quien_sale_antes,
            minutos_antes,
            mensaje_restriccion,
            rutas_ajustadas,
            advertencia_final,
        )

    if not rutas_comparten_tramos(camino_javier, camino_andreina):
        mensaje_restriccion = "Las rutas finales no comparten tramos de calle/carrera."
    else:
        aristas_javier = obtener_aristas_de_ruta(camino_javier)
        aristas_andreina = obtener_aristas_de_ruta(camino_andreina)

        # Alternativa A: Javier conserva su ruta; Andreina recalcula evitando sus aristas.
        tiempo_a_alt, camino_a_alt = calcular_ruta(
            grafo, ubicacion_andreina, destino, aristas_javier
        )
        alternativa_a = None
        if _alternativa_valida(camino_javier, camino_a_alt, tiempo_javier, tiempo_a_alt):
            alternativa_a = {
                "total": tiempo_javier + tiempo_a_alt,
                "camino_javier": list(camino_javier),
                "camino_andreina": list(camino_a_alt),
                "tiempo_javier": tiempo_javier,
                "tiempo_andreina": tiempo_a_alt,
            }

        # Alternativa B: Andreina conserva su ruta; Javier recalcula evitando sus aristas.
        tiempo_j_alt, camino_j_alt = calcular_ruta(
            grafo, ubicacion_javier, destino, aristas_andreina
        )
        alternativa_b = None
        if _alternativa_valida(camino_j_alt, camino_andreina, tiempo_j_alt, tiempo_andreina):
            alternativa_b = {
                "total": tiempo_j_alt + tiempo_andreina,
                "camino_javier": list(camino_j_alt),
                "camino_andreina": list(camino_andreina),
                "tiempo_javier": tiempo_j_alt,
                "tiempo_andreina": tiempo_andreina,
            }

        alternativas = [alt for alt in (alternativa_a, alternativa_b) if alt is not None]

        if alternativas:
            mejor = min(alternativas, key=lambda alt: alt["total"])
            camino_javier = mejor["camino_javier"]
            camino_andreina = mejor["camino_andreina"]
            tiempo_javier = mejor["tiempo_javier"]
            tiempo_andreina = mejor["tiempo_andreina"]
            rutas_ajustadas = True
            mensaje_restriccion = (
                "Se ajustaron las rutas para evitar que Javier y Andreina compartan tramos."
            )
        else:
            mensaje_restriccion = (
                "Advertencia: no se encontro una combinacion de rutas sin tramos compartidos."
            )

    if rutas_comparten_tramos(camino_javier, camino_andreina):
        advertencia_final = "Advertencia: las rutas finales todavia comparten tramos."

    if DEBUG_PRIVACIDAD:
        imprimir_debug_aristas(camino_javier, camino_andreina)

    quien_sale_antes, minutos_antes = _calcular_sincronizacion(
        tiempo_javier, tiempo_andreina
    )

    return _resultado_rutas(
        camino_javier,
        tiempo_javier,
        camino_andreina,
        tiempo_andreina,
        quien_sale_antes,
        minutos_antes,
        mensaje_restriccion,
        rutas_ajustadas,
        advertencia_final,
    )


def _resultado_rutas(
    camino_javier,
    tiempo_javier,
    camino_andreina,
    tiempo_andreina,
    quien_sale_antes,
    minutos_antes,
    mensaje_restriccion,
    rutas_ajustadas,
    advertencia_final,
):
    """Empaqueta el resultado del calculo de rutas en un diccionario."""
    return {
        "camino_javier": camino_javier,
        "tiempo_javier": tiempo_javier,
        "camino_andreina": camino_andreina,
        "tiempo_andreina": tiempo_andreina,
        "quien_sale_antes": quien_sale_antes,
        "minutos_antes": minutos_antes,
        "mensaje_restriccion": mensaje_restriccion,
        "rutas_ajustadas": rutas_ajustadas,
        "advertencia_final": advertencia_final,
    }
