"""
This module contains services for the Playlist model.

Author: yo
"""
from sqlalchemy.orm import Session
from ..models import Playlist, Song # pylint: disable=import-error

class PlaylistService:
    """
    This class represents the playlist service.
    """
    @staticmethod
    def delete_playlist(db: Session, playlist_id: int, user_id: int):
        """
        Deletes a playlist if the user is the creator.
        Args:
            db (Session): The database session
            playlist_id (int): The ID of the playlist to delete
            user_id (int): The ID of the user
        """
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()

        if playlist is None:
            raise ValueError("Playlist not found")

        if playlist.user_id != user_id:
            raise PermissionError("You are not allowed to delete this playlist")

        db.delete(playlist)
        db.commit()
        print(f'{playlist.name} has been deleted')

    @staticmethod
    def add_song_to_playlist(db: Session, playlist_id: int, song_id: int):
        """
        Adds a song to a playlist.
        Args:
            db (Session): The database session
            playlist_id (int): The ID of the playlist
            song_id (int): The ID of the song
        """
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        if playlist is None:
            raise ValueError("Playlist not found")

        song = db.query(Song).filter(Song.id == song_id).first()
        if song is None:
            raise ValueError("Song not found")

        playlist.songs.append(song)
        db.commit()
        print(f'{song.title} by {song.artist} has been added to {playlist.name}')

    @staticmethod
    def remove_song_from_playlist(db: Session, playlist_id: int, song_id: int):
        """
        Removes a song from a playlist.
        Args:
            db (Session): The database session
            playlist_id (int): The ID of the playlist
            song_id (int): The ID of the song
        """
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        if playlist is None:
            raise ValueError("Playlist not found")

        song = db.query(Song).filter(Song.id == song_id).first()
        if song is None:
            raise ValueError("Song not found")

        playlist.songs.remove(song)
        db.commit()
        print(f'{song.title} by {song.artist} has been removed from {playlist.name}')
