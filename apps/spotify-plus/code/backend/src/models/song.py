"""
This module contains the song model

Author: yo
"""
from sqlalchemy import Column, Integer, String, ForeignKey # pylint: disable=ungrouped-imports
from ..databases import Base # pylint: disable=ungrouped-imports
from sqlalchemy.orm import relationship # pylint: disable=ungrouped-imports

class Song(Base):
    """This class represents the song model"""

    __tablename__ = 'songs'
    __table_args__ = {'extend_existing': True}  # Permite redefinir la tabla
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album = Column(String)
    duration = Column(Integer)
    user_creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relación con el usuario que creó la canción
    user_creator = relationship('User', back_populates='songs')

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
