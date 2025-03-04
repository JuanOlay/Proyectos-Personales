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
    Column("playlist_id", Integer, ForeignKey("playlists.playlist_id"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.song_id"), primary_key=True),
    Column("is_favorite", Boolean, nullable=False, server_default="false"),
    extend_existing=True
)


class Playlist(Base):
    """
    This class represents the Playlist model
    """
    __tablename__ = "playlists"
    __table_args__ = {"extend_existing": True}  # eliminar cuando se haga el main.py

    playlist_id = Column(Integer, primary_key=True, index=True)
    playlist_name = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    creator = relationship("User", back_populates="created_playlists")
    queue = relationship("Queue", back_populates="playlist")  # Una playlist puede estar en la cola
    songs_in_playlist = relationship(
        "Song",
        secondary=playlist_song_association,
        back_populates="playlists_containing_song"
    )

    """
    def __init__(self, playlist_name, creator_id):
        #
        # Constructor for the Playlist model
        #
        # Args:
        #     playlist_name (str): The name of the playlist
        #     creator_id (int): The id of the user who created the playlist
        #
        self.playlist_name = playlist_name
        self.creator_id = creator_id
    """

    def __repr__(self):
        """
        Returns the string representation of the Playlist model
        """
        return f"<Playlist {self.playlist_id}>"
