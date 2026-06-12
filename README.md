# Rutas minimas en cuadricula de Bogota

Proyecto de caminos minimos para Javier y Andreina en una zona de Bogota.
Usa **Dijkstra implementado manualmente** sobre un grafo ponderado representado
con **lista de adyacencia**.

## Instalacion

Requisitos: Python 3.10 o superior.

```bash
pip install -r requirements.txt
```

`matplotlib` es opcional para el funcionamiento del programa, pero necesario
para generar la imagen `grafo_rutas.png`. Si no esta instalado, el calculo de
rutas sigue funcionando y solo se omite la visualizacion.

## Ejecucion

```bash
python main.py
```

## Estructura del proyecto

| Archivo | Contenido |
|---------|-----------|
| `main.py` | Punto de entrada del programa |
| `datos.py` | Configuracion base del enunciado y establecimientos |
| `grafo.py` | Creacion del grafo, pesos de aristas y validacion de ubicaciones |
| `dijkstra.py` | Algoritmo de Dijkstra manual, reconstruccion de camino y calculo de ruta |
| `interfaz.py` | Menu de consola, analisis de rutas y presentacion de resultados |
| `visualizacion.py` | Dibujo del grafo y rutas con matplotlib |
| `utils.py` | Utilidades: copia de configuracion, lectura por consola y formato |

## Algoritmo

- **Dijkstra** esta implementado manualmente en `dijkstra.py`, sin `networkx` ni
  otras librerias externas para resolver caminos minimos.
- El grafo se representa como **lista de adyacencia** en `grafo.py`.
- **matplotlib** se usa unicamente en `visualizacion.py` para dibujar la
  cuadricula, las vias especiales y las rutas de Javier y Andreina.

## Menu principal

1. Usar caso base del enunciado
2. Elegir establecimiento del enunciado
3. Agregar establecimiento manualmente
4. Configuracion avanzada
5. Salir

Tras calcular rutas, el programa imprime el resultado en consola y guarda
`grafo_rutas.png` si matplotlib esta disponible.

## Caso base del enunciado

- Javier: Calle 54, Carrera 14
- Andreina: Calle 52, Carrera 13
- Destino: Discoteca The Darkness (Calle 50, Carrera 14)
- Zona: Calle 50 a 55, Carrera 10 a 15
- Peso base: 5 minutos por cuadra
- Calle 51: 10 minutos
- Carreras 11, 12 y 13: 7 minutos
