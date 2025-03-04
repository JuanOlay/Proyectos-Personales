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
    __table_args__ = {'extend_existing': True}

    album_id = Column(Integer, primary_key=True)
    album_title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)

    songs_in_album = relationship("Song", back_populates="album")

    # pylint: disable=pointless-string-statement
    """
    def __init__(self, album_title, artist, release_year):
        #
        # Constructor for the Album model
        #
        # Args:
        #     album_title (str): The title of the album
        #     artist (str): The artist of the album
        #     release_year (int): The year the album was released
        #
        self.album_title = album_title
        self.artist = artist
        self.release_year = release_year
    """

    def __repr__(self):
        return f"<Album {self.album_title} by {self.artist}>"
