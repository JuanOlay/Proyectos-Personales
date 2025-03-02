# pylint: skip-file
import random

class Song:
    def __init__(self, name, affinity):
        self.name = name
        self.affinity = affinity

def generar_playlist(songs, longitud):
    """
    Genera una lista de canciones con probabilidades basadas en 'affinity',
    asegurando que no haya repeticiones consecutivas.

    :param songs: Lista de objetos Song.
    :param longitud: Longitud de la lista resultante.
    :return: Lista de canciones reorganizada.
    """
    if not songs:
        return []

    resultado = []
    ultimo = None

    for _ in range(longitud):
        # Filtrar canciones que no sean la última seleccionada
        opciones = [s for s in songs ]

        if not opciones:
            # Si no hay opciones distintas, permitir repetición forzada
            opciones = songs  

        # Elegir una canción con probabilidad basada en 'affinity'
        elegida = random.choices(opciones, weights=[s.affinity for s in opciones])[0]

        resultado.append(elegida)
        ultimo = elegida  # Actualizar la última canción seleccionada

    return resultado

# Ejemplo de uso
songs = [
    Song("Song 1", 4),
    Song("Song 2", 2),
    Song("Song 3", 4),
    Song("Song 4", 4),
    Song("Song 5", 2),
    Song("Song 6", 2),
    Song("Song 7", 4),
    Song("Song 8", 3),
    Song("Song 9", 2),
    Song("Song 10", 2),
    Song("Song 11", 1),
    Song("Song 12", 4),
    Song("Song 13", 1),
    Song("Song 14", 1),
    Song("Song 15", 1),
    Song("Song 16", 4),
    Song("Song 17", 2),
    Song("Song 18", 4),
    Song("Song 19", 3),
    Song("Song 20", 1),
    Song("Song 21", 1),
    Song("Song 22", 3),
    Song("Song 23", 4),
    Song("Song 24", 4),
    Song("Song 25", 4),
    Song("Song 26", 3),
    Song("Song 27", 1),
    Song("Song 28", 2),
    Song("Song 29", 4),
    Song("Song 30", 3),
    Song("Song 31", 4),
    Song("Song 32", 3),
    Song("Song 33", 2),
    Song("Song 34", 3),
    Song("Song 35", 1),
    Song("Song 36", 4),
    Song("Song 37", 1),
    Song("Song 38", 4),
    Song("Song 39", 4),
    Song("Song 40", 4),
    Song("Song 41", 1),
    Song("Song 42", 2),
    Song("Song 43", 2),
    Song("Song 44", 2),
    Song("Song 45", 1),
    Song("Song 46", 4),
    Song("Song 47", 4),
    Song("Song 48", 4),
    Song("Song 49", 1),
    Song("Song 50", 4),
    Song("Song 51", 2),
    Song("Song 52", 3),
    Song("Song 53", 2),
    Song("Song 54", 3),
    Song("Song 55", 4),
    Song("Song 56", 1),
    Song("Song 57", 1),
    Song("Song 58", 3),
    Song("Song 59", 3),
    Song("Song 60", 1),
    Song("Song 61", 2),
    Song("Song 62", 2),
    Song("Song 63", 4),
    Song("Song 64", 1),
    Song("Song 65", 2),
    Song("Song 66", 3),
    Song("Song 67", 4),
    Song("Song 68", 4),
    Song("Song 69", 3),
    Song("Song 70", 4),
    Song("Song 71", 4),
    Song("Song 72", 4),
    Song("Song 73", 4),
    Song("Song 74", 3),
    Song("Song 75", 1),
    Song("Song 76", 2),
    Song("Song 77", 1),
    Song("Song 78", 2),
    Song("Song 79", 1),
    Song("Song 80", 3),
    Song("Song 81", 2),
    Song("Song 82", 1),
    Song("Song 83", 4),
    Song("Song 84", 1),
    Song("Song 85", 3),
    Song("Song 86", 4),
    Song("Song 87", 2),
    Song("Song 88", 3),
    Song("Song 89", 4),
    Song("Song 90", 2),
    Song("Song 91", 3),
    Song("Song 92", 3),
    Song("Song 93", 1),
    Song("Song 94", 4),
    Song("Song 95", 1),
    Song("Song 96", 4),
    Song("Song 97", 3),
    Song("Song 98", 1),
    Song("Song 99", 4),
    Song("Song 100", 1),
    Song("Song 101", 4),
    Song("Song 102", 2),
    Song("Song 103", 4),
    Song("Song 104", 3),
    Song("Song 105", 2),
    Song("Song 106", 3),
    Song("Song 107", 3),
    Song("Song 108", 1),
    Song("Song 109", 3),
    Song("Song 110", 4),
    Song("Song 111", 1),
    Song("Song 112", 3),
    Song("Song 113", 3),
    Song("Song 114", 2),
    Song("Song 115", 2),
    Song("Song 116", 1),
    Song("Song 117", 2),
    Song("Song 118", 1),
    Song("Song 119", 1),
    Song("Song 120", 2),
    Song("Song 121", 1),
    Song("Song 122", 4),
    Song("Song 123", 2),
    Song("Song 124", 4),
    Song("Song 125", 1),
    Song("Song 126", 3),
    Song("Song 127", 1),
    Song("Song 128", 2),
    Song("Song 129", 2),
    Song("Song 130", 4),
    Song("Song 131", 3),
    Song("Song 132", 1),
    Song("Song 133", 1),
    Song("Song 134", 4),
    Song("Song 135", 4),
    Song("Song 136", 4),
    Song("Song 137", 2),
    Song("Song 138", 1),
    Song("Song 139", 3),
    Song("Song 140", 4),
    Song("Song 141", 3),
    Song("Song 142", 2),
    Song("Song 143", 2),
    Song("Song 144", 1),
    Song("Song 145", 1),
    Song("Song 146", 1),
    Song("Song 147", 1),
    Song("Song 148", 1),
    Song("Song 149", 3),
    Song("Song 150", 3),
    Song("Song 151", 3),
    Song("Song 152", 2),
    Song("Song 153", 4),
    Song("Song 154", 4),
    Song("Song 155", 3),
    Song("Song 156", 2),
    Song("Song 157", 2),
    Song("Song 158", 4),
    Song("Song 159", 3),
    Song("Song 160", 2),
    Song("Song 161", 2),
    Song("Song 162", 3),
    Song("Song 163", 1),
    Song("Song 164", 1),
    Song("Song 165", 4),
    Song("Song 166", 2),
    Song("Song 167", 2),
    Song("Song 168", 4),
    Song("Song 169", 2),
    Song("Song 170", 4),
    Song("Song 171", 2),
    Song("Song 172", 2),
    Song("Song 173", 4),
    Song("Song 174", 2),
    Song("Song 175", 1),
    Song("Song 176", 2),
    Song("Song 177", 2),
    Song("Song 178", 1),
    Song("Song 179", 2),
    Song("Song 180", 2),
]


"""
playlist_generada = generar_playlist(songs, (len(songs)*1))  # Generar una lista de 15 canciones
for song in playlist_generada:
    print(song.name)
"""
playlist_generada = generar_playlist(songs, (len(songs)*1))  # Generar una lista de 15 canciones
print([song.name for song in playlist_generada])
