"""
Menu de consola y flujo principal de la aplicacion.
"""

from datos import DESTINO_CASO_BASE, ESTABLECIMIENTOS
from dijkstra import calcular_rutas_pareja
from grafo import crear_grafo, reglas_desde_configuracion, validar_ubicacion
from utils import (
    copiar_configuracion,
    formatear_ruta,
    leer_entero,
    leer_texto,
    normalizar_destino,
    pausar,
)
from visualizacion import dibujar_grafo_y_rutas


def mostrar_resultado(resultado, destino_info):
    """Imprime el resultado en el formato solicitado para la defensa."""
    nombre_destino = destino_info["nombre"]
    calle_destino, carrera_destino = destino_info["calle"], destino_info["carrera"]

    print("\n" + "=" * 41)
    print("RESULTADO DE RUTAS")
    print("=" * 41)
    print(f"Destino: {nombre_destino}")
    print(f"Ubicacion: Calle {calle_destino} con Carrera {carrera_destino}")

    print("\nJavier:")
    print(f"Ruta: {formatear_ruta(resultado['camino_javier'])}")
    if resultado["tiempo_javier"] is not None:
        print(f"Tiempo total: {resultado['tiempo_javier']} minutos")
    else:
        print("Tiempo total: No se encontro ruta")

    print("\nAndreina:")
    print(f"Ruta: {formatear_ruta(resultado['camino_andreina'])}")
    if resultado["tiempo_andreina"] is not None:
        print(f"Tiempo total: {resultado['tiempo_andreina']} minutos")
    else:
        print("Tiempo total: No se encontro ruta")

    if resultado.get("mensaje_restriccion"):
        print("\nRestriccion de privacidad:")
        print(resultado["mensaje_restriccion"])

    if resultado.get("advertencia_final"):
        print(resultado["advertencia_final"])

    print("\nSincronizacion:")
    if resultado["quien_sale_antes"] is None:
        print("No se pudo determinar la sincronizacion (ruta no encontrada).")
    elif resultado["minutos_antes"] == 0:
        print("Ambos pueden salir al mismo tiempo.")
    else:
        otro = "Andreina" if resultado["quien_sale_antes"] == "Javier" else "Javier"
        minutos = resultado["minutos_antes"]
        unidad = "minuto" if minutos == 1 else "minutos"
        print(
            f"{resultado['quien_sale_antes']} debe salir {minutos} "
            f"{unidad} antes que {otro}."
        )

    print("=" * 41 + "\n")


def ejecutar_analisis(configuracion, destino_info):
    """Construye el grafo, calcula rutas y muestra el resultado."""
    destino_info = normalizar_destino(destino_info)
    validar_ubicacion(destino_info, configuracion, destino_info["nombre"])
    validar_ubicacion(configuracion["javier"], configuracion, "Javier")
    validar_ubicacion(configuracion["andreina"], configuracion, "Andreina")

    grafo = crear_grafo(
        configuracion["calle_min"],
        configuracion["calle_max"],
        configuracion["carrera_min"],
        configuracion["carrera_max"],
        reglas_desde_configuracion(configuracion),
    )

    destino_nodo = (destino_info["calle"], destino_info["carrera"])
    resultado = calcular_rutas_pareja(
        grafo,
        configuracion["javier"],
        configuracion["andreina"],
        destino_nodo,
    )
    mostrar_resultado(resultado, destino_info)

    dibujar_grafo_y_rutas(
        grafo,
        resultado["camino_javier"],
        resultado["camino_andreina"],
        configuracion["javier"],
        configuracion["andreina"],
        destino_nodo,
        destino_info["nombre"],
        configuracion,
    )


def mostrar_titulo():
    """Muestra el titulo del sistema al iniciar."""
    print("\nSistema de rutas secretas - Dijkstra Bogota\n")


def mostrar_menu_principal():
    """Imprime el menu principal y retorna la opcion elegida."""
    print("Menu principal:")
    print("  1. Usar caso base del enunciado")
    print("  2. Elegir establecimiento del enunciado")
    print("  3. Agregar establecimiento manualmente")
    print("  4. Configuracion avanzada")
    print("  5. Salir")
    return leer_entero("Seleccione una opcion", 1)


def mostrar_establecimientos():
    """Lista los establecimientos del enunciado."""
    print("\nEstablecimientos del enunciado:")
    for i, est in enumerate(ESTABLECIMIENTOS, start=1):
        print(
            f"  {i}. {est['nombre']} - "
            f"Calle {est['calle']} con Carrera {est['carrera']}"
        )


def seleccionar_establecimiento():
    """Permite elegir uno de los establecimientos predefinidos del enunciado."""
    mostrar_establecimientos()
    opcion = leer_entero("Seleccione el establecimiento", 1)
    if 1 <= opcion <= len(ESTABLECIMIENTOS):
        return dict(ESTABLECIMIENTOS[opcion - 1])
    print("  Opcion invalida. Se usara el primer establecimiento.")
    return dict(ESTABLECIMIENTOS[0])


def agregar_establecimiento_manual(configuracion):
    """Solicita datos de un nuevo establecimiento, valida la zona y lo retorna."""
    print("\n--- Agregar establecimiento manualmente ---")
    nombre = leer_texto("Nombre del establecimiento")
    while nombre == "":
        print("  El nombre no puede estar vacio.")
        nombre = leer_texto("Nombre del establecimiento")

    calle = leer_entero("Calle")
    carrera = leer_entero("Carrera")

    establecimiento = {"nombre": nombre, "calle": calle, "carrera": carrera}
    validar_ubicacion(establecimiento, configuracion, nombre)
    print(f"\nEstablecimiento '{nombre}' registrado correctamente.")
    return establecimiento


def editar_calles_especiales(configuracion):
    """Permite modificar los pesos especiales de calles."""
    print("\nPesos especiales de calles (movimiento horizontal).")
    print("Calles actuales:", configuracion["calles_especiales"] or "ninguna")
    print("Ingrese pares 'calle minutos'. Linea vacia para terminar.")
    print("Ejemplo: 51 10")

    nuevas_reglas = {}
    while True:
        entrada = input("  Calle y minutos (Enter para conservar actuales): ").strip()
        if entrada == "":
            break
        partes = entrada.split()
        if len(partes) == 2:
            nuevas_reglas[int(partes[0])] = int(partes[1])
        else:
            print("  Formato invalido. Use: calle minutos")

    if nuevas_reglas:
        configuracion["calles_especiales"] = nuevas_reglas
        print("  Calles especiales actualizadas:", configuracion["calles_especiales"])


def editar_carreras_especiales(configuracion):
    """Permite modificar los pesos especiales de carreras."""
    print("\nPesos especiales de carreras (movimiento vertical).")
    print("Carreras actuales:", configuracion["carreras_especiales"] or "ninguna")
    print("Ingrese pares 'carrera minutos'. Linea vacia para terminar.")
    print("Ejemplo: 11 7")

    nuevas_reglas = {}
    while True:
        entrada = input("  Carrera y minutos (Enter para conservar actuales): ").strip()
        if entrada == "":
            break
        partes = entrada.split()
        if len(partes) == 2:
            nuevas_reglas[int(partes[0])] = int(partes[1])
        else:
            print("  Formato invalido. Use: carrera minutos")

    if nuevas_reglas:
        configuracion["carreras_especiales"] = nuevas_reglas
        print("  Carreras especiales actualizadas:", configuracion["carreras_especiales"])


def editar_destino_manual():
    """Permite definir un destino manual con nombre, calle y carrera."""
    print("\n--- Destino manual ---")
    nombre = leer_texto("Nombre del destino")
    while nombre == "":
        print("  El nombre no puede estar vacio.")
        nombre = leer_texto("Nombre del destino")

    calle = leer_entero("Calle")
    carrera = leer_entero("Carrera")
    return {"nombre": nombre, "calle": calle, "carrera": carrera}


def mostrar_configuracion_actual(configuracion, destino_info=None):
    """Muestra un resumen breve de la configuracion activa."""
    print("\n--- Configuracion actual ---")
    print(
        f"Zona: Calle {configuracion['calle_min']} a {configuracion['calle_max']}, "
        f"Carrera {configuracion['carrera_min']} a {configuracion['carrera_max']}"
    )
    print(f"Peso base: {configuracion['peso_base']} minutos")
    print(f"Calles especiales: {configuracion['calles_especiales']}")
    print(f"Carreras especiales: {configuracion['carreras_especiales']}")
    print(
        f"Javier: Calle {configuracion['javier'][0]}, "
        f"Carrera {configuracion['javier'][1]}"
    )
    print(
        f"Andreina: Calle {configuracion['andreina'][0]}, "
        f"Carrera {configuracion['andreina'][1]}"
    )
    if destino_info:
        print(
            f"Destino: {destino_info['nombre']} - "
            f"Calle {destino_info['calle']} con Carrera {destino_info['carrera']}"
        )


def configuracion_avanzada(configuracion):
    """
    Submenu de configuracion avanzada. Retorna el destino elegido para calcular,
    o None si el usuario vuelve sin calcular.
    """
    destino_pendiente = None

    while True:
        mostrar_configuracion_actual(configuracion, destino_pendiente)
        print("\nConfiguracion avanzada:")
        print("  1. Cambiar limites de calles y carreras")
        print("  2. Cambiar ubicacion de Javier")
        print("  3. Cambiar ubicacion de Andreina")
        print("  4. Cambiar pesos especiales de calles")
        print("  5. Cambiar pesos especiales de carreras")
        print("  6. Ingresar destino manual")
        print("  7. Calcular rutas con la configuracion actual")
        print("  8. Volver al menu principal")

        opcion = leer_entero("Seleccione una opcion", 8)

        if opcion == 1:
            configuracion["calle_min"] = leer_entero(
                "Calle minima", configuracion["calle_min"]
            )
            configuracion["calle_max"] = leer_entero(
                "Calle maxima", configuracion["calle_max"]
            )
            configuracion["carrera_min"] = leer_entero(
                "Carrera minima", configuracion["carrera_min"]
            )
            configuracion["carrera_max"] = leer_entero(
                "Carrera maxima", configuracion["carrera_max"]
            )
            configuracion["peso_base"] = leer_entero(
                "Peso base por cuadra (minutos)", configuracion["peso_base"]
            )

        elif opcion == 2:
            calle = leer_entero("Calle de Javier", configuracion["javier"][0])
            carrera = leer_entero("Carrera de Javier", configuracion["javier"][1])
            configuracion["javier"] = (calle, carrera)

        elif opcion == 3:
            calle = leer_entero("Calle de Andreina", configuracion["andreina"][0])
            carrera = leer_entero("Carrera de Andreina", configuracion["andreina"][1])
            configuracion["andreina"] = (calle, carrera)

        elif opcion == 4:
            editar_calles_especiales(configuracion)

        elif opcion == 5:
            editar_carreras_especiales(configuracion)

        elif opcion == 6:
            destino_pendiente = editar_destino_manual()

        elif opcion == 7:
            if destino_pendiente is None:
                print("\nNo hay destino definido. Elija uno:")
                print("  1. Usar destino del caso base")
                print("  2. Elegir establecimiento del enunciado")
                print("  3. Ingresar destino manual")
                sub = leer_entero("Opcion", 1)
                if sub == 1:
                    destino_pendiente = normalizar_destino(dict(DESTINO_CASO_BASE))
                elif sub == 2:
                    destino_pendiente = seleccionar_establecimiento()
                else:
                    destino_pendiente = editar_destino_manual()
            return destino_pendiente

        elif opcion == 8:
            return None

        else:
            print("  Opcion invalida.")


def ejecutar_caso_base():
    """Ejecuta el caso base del enunciado sin preguntas adicionales."""
    configuracion = copiar_configuracion()
    destino = normalizar_destino(dict(DESTINO_CASO_BASE))
    print("\nUsando caso base del enunciado...")
    print(
        f"Destino: {destino['nombre']} "
        f"(Calle {destino['calle']}, Carrera {destino['carrera']})"
    )
    ejecutar_analisis(configuracion, destino)


def ejecutar_menu():
    """Punto de entrada: menu principal en bucle hasta que el usuario salga."""
    mostrar_titulo()
    configuracion_activa = copiar_configuracion()

    while True:
        try:
            opcion = mostrar_menu_principal()

            if opcion == 1:
                ejecutar_caso_base()
                pausar()

            elif opcion == 2:
                configuracion = copiar_configuracion()
                destino = seleccionar_establecimiento()
                ejecutar_analisis(configuracion, destino)
                pausar()

            elif opcion == 3:
                destino = agregar_establecimiento_manual(configuracion_activa)
                ejecutar_analisis(configuracion_activa, destino)
                pausar()

            elif opcion == 4:
                destino = configuracion_avanzada(configuracion_activa)
                if destino is not None:
                    ejecutar_analisis(configuracion_activa, destino)
                    pausar()

            elif opcion == 5:
                print("\nHasta luego!\n")
                break

            else:
                print("  Opcion invalida. Elija un numero del 1 al 5.")

        except ValueError as error:
            print(f"\nError: {error}")
            pausar()
        except KeyboardInterrupt:
            print("\n\nPrograma cancelado por el usuario.\n")
            break
