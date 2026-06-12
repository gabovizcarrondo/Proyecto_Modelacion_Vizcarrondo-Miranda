"""
Visualizacion del grafo y las rutas con matplotlib.
Genera grafo_tecnico.png y mapa_limpio.png.
"""


def limpiar_nombre_archivo(nombre):
    import re
    limpio = re.sub(r"[^\w\s-]", "", nombre, flags=re.UNICODE).strip()
    limpio = re.sub(r"\s+", "_", limpio)
    return limpio or "grafico"


def nodo_a_coordenadas(nodo):
    calle, carrera = nodo
    return carrera, calle


def arista_unica(nodo_a, nodo_b):
    return tuple(sorted((nodo_a, nodo_b)))


def dibujar_segmento_ruta(ax, nodo_a, nodo_b, color, grosor, desplazamiento, estilo="-", etiqueta=None):
    x1, y1 = nodo_a_coordenadas(nodo_a)
    x2, y2 = nodo_a_coordenadas(nodo_b)
    if y1 == y2:
        y1 += desplazamiento
        y2 += desplazamiento
    elif x1 == x2:
        x1 += desplazamiento
        x2 += desplazamiento
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=grosor, linestyle=estilo,
            label=etiqueta, zorder=7, solid_capstyle="round", alpha=0.95)


def etiqueta_con_fondo(ax, texto, nodo, desplazamiento, color_texto, tamano=8):
    x, y = nodo_a_coordenadas(nodo)
    ax.annotate(texto, (x, y), textcoords="offset points", xytext=desplazamiento,
                fontsize=tamano, fontweight="bold", color=color_texto, zorder=10,
                ha="center", va="top" if desplazamiento[1] < 0 else "bottom",
                bbox={"boxstyle": "round,pad=0.3", "facecolor": "white",
                      "edgecolor": "#cccccc", "alpha": 0.92, "linewidth": 0.5})


def configurar_ejes(ax, configuracion):
    calle_min, calle_max = configuracion["calle_min"], configuracion["calle_max"]
    carrera_min, carrera_max = configuracion["carrera_min"], configuracion["carrera_max"]
    margen = 0.35
    ax.set_xlim(carrera_min - margen, carrera_max + margen)
    ax.set_ylim(calle_min - margen, calle_max + margen)
    ax.invert_xaxis()
    ax.set_xticks(range(carrera_min, carrera_max + 1))
    ax.set_yticks(range(calle_min, calle_max + 1))
    ax.tick_params(axis="both", labelsize=8, colors="#666666", length=3, width=0.5)
    ax.set_xlabel("Carrera (este -> oeste)", fontsize=9, color="#555555", labelpad=4)
    ax.set_ylabel("Calle (sur -> norte)", fontsize=9, color="#555555", labelpad=4)
    ax.grid(True, linestyle=":", color="#dddddd", linewidth=0.6, alpha=0.7, zorder=0)
    ax.set_aspect("equal", adjustable="box")
    for borde in ax.spines.values():
        borde.set_color("#cccccc")
        borde.set_linewidth(0.6)


def dibujar_aristas(grafo, ax):
    aristas_vistas = set()
    for nodo, vecinos in grafo.items():
        for vecino, _ in vecinos:
            clave = arista_unica(nodo, vecino)
            if clave in aristas_vistas:
                continue
            aristas_vistas.add(clave)
            x1, y1 = nodo_a_coordenadas(nodo)
            x2, y2 = nodo_a_coordenadas(vecino)
            ax.plot([x1, x2], [y1, y2], color="#d8d8d8", linewidth=0.9, zorder=1, alpha=0.9)


def dibujar_nodos(grafo, ax):
    for nodo in grafo:
        x, y = nodo_a_coordenadas(nodo)
        ax.plot(x, y, "o", color="#4a4a4a", markersize=4.5,
                markeredgecolor="white", markeredgewidth=0.3, zorder=3)


def dibujar_vias_lentas(ax, configuracion):
    calle_min, calle_max = configuracion["calle_min"], configuracion["calle_max"]
    carrera_min, carrera_max = configuracion["carrera_min"], configuracion["carrera_max"]
    for calle in configuracion.get("calles_especiales", {}):
        if calle_min <= calle <= calle_max:
            ax.plot([carrera_min, carrera_max], [calle, calle],
                    color="#e8b86d", linewidth=7, alpha=0.4, zorder=2, solid_capstyle="butt")
    for carrera in configuracion.get("carreras_especiales", {}):
        if carrera_min <= carrera <= carrera_max:
            ax.plot([carrera, carrera], [calle_min, calle_max],
                    color="#c9a0dc", linewidth=7, alpha=0.38, zorder=2, solid_capstyle="butt")


def dibujar_rutas(ax, ruta_javier, ruta_andreina, cj, ca):
    if len(ruta_javier) >= 2:
        for i in range(len(ruta_javier) - 1):
            dibujar_segmento_ruta(ax, ruta_javier[i], ruta_javier[i + 1],
                                  cj, 4.5, 0.035, etiqueta="Ruta Javier" if i == 0 else None)
    if len(ruta_andreina) >= 2:
        for i in range(len(ruta_andreina) - 1):
            dibujar_segmento_ruta(ax, ruta_andreina[i], ruta_andreina[i + 1],
                                  ca, 4.5, -0.035, estilo=(0, (4, 2)),
                                  etiqueta="Ruta Andreina" if i == 0 else None)


def dibujar_marcadores(ax, origen_javier, origen_andreina, destino, nombre_destino, cj, ca, cd):
    puntos = [
        (origen_javier, "Javier", cj, "s", 12, (-12, 10)),
        (origen_andreina, "Andreina", ca, "s", 12, (12, 10)),
        (destino, nombre_destino, cd, "*", 18, (0, -18)),
    ]
    for nodo, etiqueta, color, marcador, tamano, desplazamiento in puntos:
        x, y = nodo_a_coordenadas(nodo)
        ax.plot(x, y, marker=marcador, color=color, markersize=tamano,
                markeredgecolor="#333333", markeredgewidth=0.8, zorder=9)
        etiqueta_con_fondo(ax, etiqueta, nodo, desplazamiento, color,
                           tamano=7 if len(etiqueta) > 14 else 8)


def agregar_leyenda(ax, cj, ca, cd, configuracion):
    from matplotlib.lines import Line2D
    calles = configuracion.get("calles_especiales", {})
    carreras = configuracion.get("carreras_especiales", {})
    elementos = [
        Line2D([0], [0], color=cj, linewidth=4, label="Ruta Javier"),
        Line2D([0], [0], color=ca, linewidth=4, linestyle=(0, (4, 2)), label="Ruta Andreina"),
        Line2D([0], [0], marker="s", color=cj, markersize=8, linestyle="None",
               markeredgecolor="#333333", label="Javier"),
        Line2D([0], [0], marker="s", color=ca, markersize=8, linestyle="None",
               markeredgecolor="#333333", label="Andreina"),
        Line2D([0], [0], marker="*", color=cd, markersize=12, linestyle="None",
               markeredgecolor="#333333", label="Destino"),
    ]
    if calles:
        c, m = next(iter(sorted(calles.items())))
        elementos.append(Line2D([0], [0], color="#e8b86d", linewidth=5, alpha=0.6,
                                label=f"Calle {c}: {m} min"))
    if carreras:
        nums = sorted(carreras.keys())
        m = carreras[nums[0]]
        if len(nums) == 1:
            txt = f"Carrera {nums[0]}: {m} min"
        elif len(nums) == 2:
            txt = f"Carreras {nums[0]} y {nums[1]}: {m} min"
        else:
            txt = f"Carreras {', '.join(map(str, nums[:-1]))} y {nums[-1]}: {m} min"
        elementos.append(Line2D([0], [0], color="#c9a0dc", linewidth=5, alpha=0.6, label=txt))
    ax.legend(handles=elementos, loc="upper left", bbox_to_anchor=(1.02, 1.0),
              fontsize=7.5, frameon=True, framealpha=0.95, edgecolor="#dddddd")


def agregar_titulos(fig, ax, nombre_destino, configuracion):
    cm, cx = configuracion["calle_min"], configuracion["calle_max"]
    rm, rx = configuracion["carrera_min"], configuracion["carrera_max"]
    ax.set_title(f"Rutas minimas hacia {nombre_destino}", fontsize=12,
                 fontweight="bold", color="#222222", pad=10)
    ax.text(0.5, 1.02, f"Grafo ponderado de la zona Calle {cm}-{cx} y Carrera {rm}-{rx}",
            transform=ax.transAxes, ha="center", fontsize=8, color="#777777")
    fig.text(0.5, 0.01, "Los pesos representan minutos por cuadra. Dijkstra calcula las rutas minimas.",
             ha="center", fontsize=7.5, color="#888888")


def _generar_figura(grafo, ruta_javier, ruta_andreina, origen_javier, origen_andreina,
                    destino, nombre_destino, configuracion, modo="tecnico"):
    import matplotlib.pyplot as plt
    cj, ca, cd = "#2563eb", "#dc2626", "#16a34a"
    fig, ax = plt.subplots(figsize=(9, 7))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    configurar_ejes(ax, configuracion)
    if modo == "tecnico":
        dibujar_aristas(grafo, ax)
        dibujar_nodos(grafo, ax)
        dibujar_vias_lentas(ax, configuracion)
    else:
        dibujar_vias_lentas(ax, configuracion)
        for calle in range(configuracion["calle_min"], configuracion["calle_max"] + 1):
            ax.axhline(calle, color="#ececec", linewidth=0.8, zorder=0)
        for carrera in range(configuracion["carrera_min"], configuracion["carrera_max"] + 1):
            ax.axvline(carrera, color="#ececec", linewidth=0.8, zorder=0)
    dibujar_rutas(ax, ruta_javier, ruta_andreina, cj, ca)
    dibujar_marcadores(ax, origen_javier, origen_andreina, destino, nombre_destino, cj, ca, cd)
    agregar_leyenda(ax, cj, ca, cd, configuracion)
    agregar_titulos(fig, ax, nombre_destino, configuracion)
    return fig


def dibujar_grafo_y_rutas(grafo, ruta_javier, ruta_andreina, origen_javier, origen_andreina,
                          destino, nombre_destino, configuracion):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("No se pudo generar la visualizacion porque matplotlib no esta instalado.")
        return
    for nombre_archivo, modo in [("grafo_tecnico.png", "tecnico"), ("mapa_limpio.png", "limpio")]:
        fig = _generar_figura(grafo, ruta_javier, ruta_andreina, origen_javier, origen_andreina,
                              destino, nombre_destino, configuracion, modo=modo)
        fig.tight_layout()
        fig.subplots_adjust(right=0.72, bottom=0.08, top=0.90)
        fig.savefig(nombre_archivo, dpi=220, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        print(f"Visualizacion guardada como {nombre_archivo}")
