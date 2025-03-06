"""
This module contains the song model

Author: yo
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # pylint: disable=ungrouped-imports
from sqlalchemy.orm import relationship # pylint: disable=ungrouped-imports
from ..databases import Base
from .playlist import playlist_song_association
from .queue import queue_song_association
from .user import user_song_affinity


class Song(Base):
    """This class represents the song model"""

    __tablename__ = 'songs'
    __table_args__ = {"extend_existing": True}

    song_id = Column(Integer, primary_key=True)
    song_title = Column(String, nullable=False)
    song_data = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey("albums.album_id"))
    duration = Column(Integer, nullable=False)
    mark_as_favorite = Column(Boolean, default=False)
    creator_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    creator = relationship("User", back_populates="created_songs")
    in_queues = relationship("Queue",
        secondary=queue_song_association,
        back_populates="queue_songs"
        )
    playlists_containing_song = relationship(
        "Playlist",
        secondary=playlist_song_association,
        back_populates="songs_in_playlist"
    )
    users_with_affinity = relationship(
        "User",
        secondary=user_song_affinity,
        back_populates="song_affinities"
        )
    history = relationship("History", back_populates="song")
    album = relationship("Album", back_populates="songs_in_album")

    def __repr__(self):
        return f"<Song {self.song_title} by {self.artist}>"
