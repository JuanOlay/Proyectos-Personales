# pylint: skip-file
import ast
from collections import Counter
import re

def extraer_numero(cancion):
    """Extrae el número de una canción si tiene un formato tipo 'Song 1', 'Song 10', etc."""
    # Busca números al final del nombre de la canción
    match = re.search(r'(\d+)$', cancion)
    if match:
        return int(match.group(1))
    return cancion  # Si no encuentra números, mantiene el nombre tal cual

def analizar_probabilidad(archivo):
    """Lee un archivo de texto y calcula la probabilidad de aparición de cada canción, expresada en un rango de 1 a 5."""
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            contenido = file.read().strip()
            
            # Intentar interpretar como lista si está en formato de lista de Python
            if contenido.startswith("[") and contenido.endswith("]"):
                try:
                    datos = ast.literal_eval(contenido)
                    if not isinstance(datos, list) or not all(isinstance(i, str) for i in datos):
                        raise ValueError("El archivo no contiene una lista de cadenas válida.")
                except (SyntaxError, ValueError) as e:
                    print(f"Error al interpretar el contenido del archivo: {e}")
                    return
            else:
                datos = contenido.splitlines()
            
            if not datos:
                print("El archivo está vacío o no contiene datos válidos.")
                return
            
            # Contar ocurrencias de cada canción en toda la lista
            conteo_total = Counter(datos)
            total_canciones = len(datos)

            # Evitar división por cero
            if total_canciones == 0:
                print("No hay suficientes datos para calcular probabilidades.")
                return

            # Normalizar valores a un rango de 1 a 5 proporcionalmente
            max_conteo = max(conteo_total.values())
            min_conteo = min(conteo_total.values())

            if max_conteo == min_conteo:  # Todas las canciones aparecen la misma cantidad de veces
                probabilidades = {song: 3 for song in conteo_total}
            else:
                probabilidades = {
                    song: round(1 + (conteo - min_conteo) * 4 / (max_conteo - min_conteo))
                    for song, conteo in conteo_total.items()
                }

            # Mostrar resultados ordenados alfabéticamente por nombre de canción,
            # considerando los números correctamente
            print("Probabilidad de aparición de cada canción (1-5):")
            for song in sorted(probabilidades.keys(), key=extraer_numero):
                print(f"{song}: {probabilidades[song]}")

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

# Uso del programa
documento = "Experimento/xd.txt"
analizar_probabilidad(documento)
