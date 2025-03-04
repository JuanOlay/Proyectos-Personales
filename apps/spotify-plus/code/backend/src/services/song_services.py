"""
This is the service module for the song model.

Author: yomerito
"""
import os  # pylint: disable=wrong-import-order
import time  # pylint: disable=import-error
import base64
import tempfile
import logging
from mutagen.mp3 import MP3  # pylint: disable=import-error
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.song import Song
import vlc  # pylint: disable=import-error, wrong-import-order

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SongService:
    """
    This class represents the song service.
    """
    @staticmethod
    def get_audio_metadata(file_path):
        """Obtiene la duración del archivo de audio usando mutagen."""
        try:
            audio = MP3(file_path)
            return int(audio.info.length)  # Duración en segundos
        except Exception as e:
            logging.error("Error al obtener metadatos de %s: %s", file_path, e)
            return None

    @staticmethod
    def add_song(db: Session, file_path, song_title, artist, album_id, creator_user_id):
        """Agrega una canción a la base de datos con sus metadatos y el contenido codificado."""
        if not os.path.exists(file_path):
            logging.error("Error: El archivo %s no existe.", file_path)
            return None

        duration = SongService.get_audio_metadata(file_path)
        if duration is None:
            logging.error("Error: No se pudo obtener la duración del archivo %s.", file_path)
            return None

        # Leer el contenido del archivo en modo binario y codificarlo en base64
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            encoded_data = base64.b64encode(data).decode("utf-8")
        except OSError as e:
            logging.error("Error al leer el archivo %s: %s", file_path, e)
            return None

        try:
            new_song = Song(
                song_title=song_title,
                song_data=encoded_data,
                artist=artist,
                album_id=album_id,
                duration=duration,
                creator_user_id=creator_user_id
            )

            db.add(new_song)
            db.commit()
            db.refresh(new_song)
            logging.info("Canción '%s' agregada con éxito.", song_title)
            return new_song
        except SQLAlchemyError as e:
            db.rollback()
            logging.error("Error al agregar la canción '%s': %s", song_title, e)
            return None
        finally:
            db.close()

    @staticmethod
    def play_song(db: Session, song_id: int):
        """Reproduce una canción almacenada en la base de datos usando VLC."""
        try:
            song = db.query(Song).filter(Song.song_id == song_id).first()
            if not song:
                logging.error("Error: Canción con ID %d no encontrada.", song_id)
                return

            # Decodificar los datos de la canción de base64 a binario
            song_binary = base64.b64decode(song.song_data)
        except (SQLAlchemyError, base64.binascii.Error) as e:
            logging.error("Error al recuperar o decodificar la canción con ID %d: %s", song_id, e)
            return
        finally:
            db.close()

        # Escribir el contenido en un archivo temporal
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(song_binary)
                temp_file_path = tmp_file.name
        except OSError as e:
            logging.error("Error al crear el archivo temporal: %s", e)
            return

        try:
            player = vlc.MediaPlayer(temp_file_path)
            player.play()

            time.sleep(1)  # Pequeña pausa antes de verificar el estado de reproducción
            while player.get_state() not in [vlc.State.Ended, vlc.State.Stopped]:
                time.sleep(1)
        except Exception as e:
            logging.error("Error al reproducir %s: %s", temp_file_path, e)

    @staticmethod
    def delete_song(db: Session, song_id: int):
        """Elimina una canción de la base de datos."""
        try:
            song = db.query(Song).filter(Song.song_id == song_id).first()
            if not song:
                logging.error("Error: Canción con ID %d no encontrada.", song_id)
                return None

            db.delete(song)
            db.commit()
            logging.info("Canción '%s' eliminada con éxito.", song.song_title)
            return song
        except SQLAlchemyError as e:
            db.rollback()
            logging.error("Error al eliminar la canción con ID %d: %s", song_id, e)
            return None
        finally:
            db.close()
