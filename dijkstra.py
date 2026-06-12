"""
Algoritmo de Dijkstra implementado manualmente (sin librerias externas).
"""


def dijkstra(grafo, origen, destino):
    """
    Encuentra la distancia minima desde origen hasta destino.

    Retorna (distancia_minima, predecesores). Si no hay ruta, distancia_minima es None.
    """
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


def calcular_ruta(grafo, origen, destino):
    """
    Calcula la ruta minima entre dos nodos.

    Retorna (tiempo_total, camino).
    """
    tiempo, predecesores = dijkstra(grafo, origen, destino)
    camino = reconstruir_camino(predecesores, origen, destino)
    return tiempo, camino
