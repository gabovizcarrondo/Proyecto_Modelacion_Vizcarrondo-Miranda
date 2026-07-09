"""
Script temporal de auditoria: compara calcular_rutas_pareja (heuristica A/B)
con busqueda exhaustiva de pares entre k-mejores rutas de cada persona.
"""

from itertools import product

from datos import CONFIGURACION_BASE
from dijkstra import (
    calcular_ruta,
    calcular_rutas_pareja,
    obtener_aristas_de_ruta,
    rutas_comparten_tramos,
)
from grafo import crear_grafo, reglas_desde_configuracion

K = 8  # cantidad de mejores rutas por persona a considerar


def construir_grafo():
    reglas = reglas_desde_configuracion(CONFIGURACION_BASE)
    return crear_grafo(
        CONFIGURACION_BASE["calle_min"],
        CONFIGURACION_BASE["calle_max"],
        CONFIGURACION_BASE["carrera_min"],
        CONFIGURACION_BASE["carrera_max"],
        reglas,
    )


def k_mejores_rutas(grafo, origen, destino, k=K):
    """
    Encuentra hasta k rutas simples distintas ordenadas por costo,
    bloqueando una arista de cada ruta encontrada para forzar alternativas.
    """
    rutas = []
    vistos = set()
    aristas_bloqueadas = set()

    for _ in range(k):
        tiempo, camino = calcular_ruta(grafo, origen, destino, aristas_bloqueadas)
        if tiempo is None or not camino:
            break
        clave = tuple(camino)
        if clave not in vistos:
            vistos.add(clave)
            rutas.append((tiempo, list(camino)))

        # Bloquear una arista de la ruta minima actual para obtener la siguiente
        bloqueo_agregado = False
        for i in range(len(camino) - 1):
            from dijkstra import arista_canonica

            arista = arista_canonica(camino[i], camino[i + 1])
            if arista not in aristas_bloqueadas:
                aristas_bloqueadas.add(arista)
                bloqueo_agregado = True
                break
        if not bloqueo_agregado:
            break

    return rutas


def busqueda_exhaustiva(grafo, origen_j, origen_a, destino, k=K):
    rutas_j = k_mejores_rutas(grafo, origen_j, destino, k)
    rutas_a = k_mejores_rutas(grafo, origen_a, destino, k)

    mejor = None
    for tj, cj in rutas_j:
        for ta, ca in rutas_a:
            if rutas_comparten_tramos(cj, ca):
                continue
            total = tj + ta
            candidato = {
                "total": total,
                "tiempo_javier": tj,
                "tiempo_andreina": ta,
                "camino_javier": cj,
                "camino_andreina": ca,
            }
            if mejor is None or total < mejor["total"]:
                mejor = candidato
    return mejor, len(rutas_j), len(rutas_a)


def generar_combinaciones():
    cmin, cmax = CONFIGURACION_BASE["calle_min"], CONFIGURACION_BASE["calle_max"]
    rmin, rmax = CONFIGURACION_BASE["carrera_min"], CONFIGURACION_BASE["carrera_max"]
    javier = CONFIGURACION_BASE["javier"]
    andreina = CONFIGURACION_BASE["andreina"]

    destinos = [
        (50, 14),
        (54, 11),
        (50, 12),
        (55, 15),
        (50, 10),
        (55, 10),
    ]

    origenes = [javier, andreina, (54, 13), (52, 14), (53, 12), (51, 11)]

    casos = set()
    for dest in destinos:
        casos.add((javier, andreina, dest))
        for oj in origenes:
            for oa in origenes:
                if oj != oa:
                    casos.add((oj, oa, dest))

    return sorted(casos)


def main():
    grafo = construir_grafo()
    contraejemplos = []
    iguales = 0
    sin_exhaustivo = 0

    for origen_j, origen_a, destino in generar_combinaciones():
        heuristica = calcular_rutas_pareja(grafo, origen_j, origen_a, destino)
        total_h = (heuristica["tiempo_javier"] or 0) + (
            heuristica["tiempo_andreina"] or 0
        )
        if heuristica["tiempo_javier"] is None or heuristica["tiempo_andreina"] is None:
            continue

        exhaustivo, nj, na = busqueda_exhaustiva(grafo, origen_j, origen_a, destino)
        if exhaustivo is None:
            sin_exhaustivo += 1
            continue

        total_e = exhaustivo["total"]
        if total_e < total_h:
            contraejemplos.append(
                {
                    "origen_javier": origen_j,
                    "origen_andreina": origen_a,
                    "destino": destino,
                    "total_heuristica": total_h,
                    "total_exhaustivo": total_e,
                    "heuristica": heuristica,
                    "exhaustivo": exhaustivo,
                    "rutas_j_exploradas": nj,
                    "rutas_a_exploradas": na,
                }
            )
        else:
            iguales += 1

    print(f"Casos comparados (con solucion exhaustiva): {iguales + len(contraejemplos)}")
    print(f"Casos sin par valido en k={K} rutas: {sin_exhaustivo}")
    print(f"Contraejemplos encontrados: {len(contraejemplos)}")

    if contraejemplos:
        c = min(contraejemplos, key=lambda x: x["total_exhaustivo"] - x["total_heuristica"])
        print("\n=== CONTRAEJEMPLO ===")
        print(f"Javier origen: {c['origen_javier']}")
        print(f"Andreina origen: {c['origen_andreina']}")
        print(f"Destino: {c['destino']}")
        print(f"\nHeuristica A/B - total {c['total_heuristica']} min")
        print(f"  Javier ({c['heuristica']['tiempo_javier']}): {c['heuristica']['camino_javier']}")
        print(
            f"  Andreina ({c['heuristica']['tiempo_andreina']}): "
            f"{c['heuristica']['camino_andreina']}"
        )
        print(f"\nExhaustivo k={K} - total {c['total_exhaustivo']} min")
        print(f"  Javier ({c['exhaustivo']['tiempo_javier']}): {c['exhaustivo']['camino_javier']}")
        print(
            f"  Andreina ({c['exhaustivo']['tiempo_andreina']}): "
            f"{c['exhaustivo']['camino_andreina']}"
        )
        print(f"\nAhorro exhaustivo: {c['total_heuristica'] - c['total_exhaustivo']} min")
    else:
        print(
            f"\nNo se encontro contraejemplo con k={K} mejores rutas por persona "
            f"en la cuadricula del enunciado."
        )


if __name__ == "__main__":
    main()
