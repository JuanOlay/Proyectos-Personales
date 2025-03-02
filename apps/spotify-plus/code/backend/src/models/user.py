""" 
Este módulo representa el modelo de usuario

Author: yo
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..databases import Base # pylint: disable=import-error

class User (Base):

    """This class represents the user model"""
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}  # Permite redefinir la tabla

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    created_songs = relationship('Song', back_populates='creator')
    credentials = relationship("UserCredentials", uselist=False, back_populates="user")
    created_playlists = relationship("Playlist", back_populates="creator")

    def __init__(self, username : str, email: str, password: str):
        """
        This method is used to initialize the user model
        
        Args:
            username (str): The username of the user
            email (str): The email of the user
            password (str): The password of the user
        """

        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        """
        This method is used to represent the user model as a string
        """

        return f'<User {self.username}>'
