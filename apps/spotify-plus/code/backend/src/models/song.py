"""
This module contains the song model

Author: yo
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table # pylint: disable=ungrouped-imports
from sqlalchemy.orm import relationship # pylint: disable=ungrouped-imports
from ..databases import Base # pylint: disable=import-error

# Tabla intermedia para la relación Playlist-Song (muchos a muchos)
playlist_song_association = Table(
    "playlist_song_association",
    Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.playlist_id"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.song_id"), primary_key=True)
)

class Song(Base):
    """This class represents the song model"""

    __tablename__ = 'songs'
    __table_args__ = {'extend_existing': True}  # Permite redefinir la tabla

    song_id = Column(Integer, primary_key=True)
    song_title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album = Column(String)
    duration = Column(Integer)
    mark_as_favorite = Column(Boolean, default=False)
    creator_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    creator = relationship("User", back_populates="created_songs")
    playlists_containing_song = relationship(
        "Playlist",
        secondary=playlist_song_association,
        back_populates="songs_in_playlist"
    )

    def __init__(self, title : str, artist: str, album: str, duration: float, user_creator_id: int):
        """
        This mehod is used to initialize the song model
        
        Args:
            title (str): The title of the song
            artist (str): The artist of the song
            album (str): The album of the song
            duration (int): The duration of the song
        """

        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.user_creator_id = user_creator_id

    def __repr__(self):
        """
        This method is used to represent the song model as a string
        """

        return f'<Song {self.title} by {self.artist}>'
