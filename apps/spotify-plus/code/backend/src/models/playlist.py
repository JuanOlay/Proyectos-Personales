"""
This module contains the Playlist model.

Author: yo
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..databases import Base

# Tabla intermedia para la relación muchos a muchos entre Playlist y Song
playlist_song_association = Table(
    "playlist_song",
    Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
    Column("is_favorite", Boolean, default=False)# Indica si la canción es favorita en esa playlist
)

class Playlist(Base):
    """
    This class represents the Playlist model
    """
    __tablename__ = "playlists"

    playlist_id = Column(Integer, primary_key=True, index=True)
    playlist_name = Column(String, nullable=False)

    creator_user_id = relationship("User", back_populates="crated_playlists")
    songs_in_playlist = relationship("Song", secondary=playlist_song_association, back_populates="playlists_containing_song")

    def __init__(self, name: str, creator_id: int, songs: list):
        """
        This method is used to initialize the Playlist model

        Args:
            name (str): The name of the playlist
            creator_id (int): The ID of the user who created the playlist
        """

        self.name = name
        self.creator_id = creator_id
        self.songs = songs
