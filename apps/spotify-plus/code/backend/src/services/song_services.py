"""
This module contains the song services.

Author: yomero
"""
import os
import base64
import tempfile
import logging
import pygame
from mutagen import MutagenError
from mutagen.mp3 import MP3
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.song import Song
from .user_services import User

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SongService:
    """
    This class represents the song service.
    """
    pygame.mixer.init()

    # Define global variables
    playlist = []  # List to store names of songs
    current_song = ""  # Store the currently playing song
    is_paused = False  # Flag to indicate if music is paused

    @staticmethod
    def get_audio_metadata(file_path) -> int:
        """
        Obtiene la duración del archivo de audio usando mutagen.
        
        Args:
            file_path (str): La ruta del archivo de audio
        """
        if not os.path.isfile(file_path):
            logging.error("El archivo %s no existe.", file_path)
            return None

        try:
            audio = MP3(file_path)
            return int(audio.info.length)  # Duración en segundos
        except MutagenError as e:
            logging.error(
                "Error de Mutagen al obtener metadatos de %s: %s",
                file_path,
                e
                )
        return None

    @staticmethod
    def add_song(
        db: Session,
        file_path : str ,
        song_title : str,
        artist : str,
        album_id : int,
        current_user : User
        ) -> Song:
        """
        Agrega una canción a la base de datos con sus metadatos y el contenido codificado.
        
        Args:
            db (Session): La sesión de la base de datos
            file_path (str): La ruta del archivo de audio
            song_title (str): El título de la canción
            artist (str): El nombre del artista
            album_id (int): El ID del álbum
            current_user (User): El usuario que agrega la canción
        """
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
                creator_user_id=current_user.user_id
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

    @staticmethod
    def play_song(db: Session, song_id: int):
        """
        Reproduce una canción almacenada en la base de datos usando pygame.
        
        Args:
            db (Session): La sesión de la base de datos
            song_id (int): El ID de la canción a reproducir
        """
        try:
            song = db.query(Song).filter(Song.song_id == song_id).first()
            if not song:
                logging.error("Error: Canción con ID %d no encontrada.", song_id)
                return

            # Decodificar los datos de la canción de base64 a binario
            song_binary = base64.b64decode(song.song_data)
        except (SQLAlchemyError, base64.binascii.Error) as e:
            logging.error(
                "Error al recuperar o decodificar la canción con ID %d: %s",
                song_id,
                e
            )
            return

        # Escribir el contenido en un archivo temporal
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(song_binary)
                temp_file_path = tmp_file.name
        except OSError as e:
            logging.error("Error al crear el archivo temporal: %s", e)
            return

        if SongService.is_paused:
            # Si la canción está pausada, solo la reanudamos
            pygame.mixer.music.unpause()
            SongService.is_paused = False
            return

        try:
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()
        except pygame.error as e: # pylint: disable=no-member
            logging.error("Error al cargar o reproducir la canción: %s", e)


    @staticmethod
    def delete_song(db: Session, song_id: int):
        """
        Elimina una canción de la base de datos.
        
        Args:
            db (Session): La sesión de la base de datos
            song_id (int): El ID de la canción a eliminar
        """
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

    @staticmethod
    def pause_song():
        """
        Pausa la reproducción de la canción.
        """
        pygame.mixer.music.pause()
        SongService.is_paused = True
