"""
This snippet from apps/spotify-plus/code/backend/src/services/song_services.py:

Author: yomerito
"""
from sqlalchemy.orm import Session
from ..models import Song # pylint: disable=import-error

class SongService:
    """
    This class represents the song service.
    """
    @staticmethod
    def delete_song(db: Session, song_id: int, user_id: int):
        """
        Deletes a song if the user is the creator.
        Args:
            db (Session): The database session
            song_id (int): The ID of the song to delete
            user_id (int): The ID of the user
        """
        song = db.query(Song).filter(Song.id == song_id).first()

        if song is None:
            raise ValueError("Song not found")

        if song.user_creator_id != user_id:
            raise PermissionError("You are not allowed to delete this song")

        db.delete(song)
        db.commit()
        print(f'{song.title} by {song.artist} has been deleted')

    @staticmethod
    def play_song(db : Session, song_id: int):
        """
        Simula la reproducción de una canción
        Args:
            db (Session): The database session
            song_id (int): The ID of the song to play
        """
        song = db.query(Song).filter(Song.id == song_id).first()
        if not song:
            raise ValueError("Song not found")

        print(f'🎵 Playing "{song.title}" by {song.artist}...')
        # Aquí puedes agregar la lógica para manejar el streaming de audio
