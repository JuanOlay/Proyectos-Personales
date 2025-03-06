"""
This is the album model. It is used to store the albums of the songs.

Author: yo"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..databases import Base

class Album(Base):
    """
    This class represents the album model
    """
    __tablename__ = 'albums'
    __table_args__ = {'extend_existing': True} # eliminar cuando se haga el main.py

    album_id = Column(Integer, primary_key=True)
    album_title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)

    songs_in_album = relationship("Song", back_populates="album")

    def __repr__(self):
        return f"<Album {self.album_title} by {self.artist}>"
