""" 
Este módulo representa el modelo de usuario

Author: yo
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.databases import Base # pylint: disable=import-error

class User (Base):

    """This class represents the user model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    songs = relationship('Song', back_populates='user_creator')
    credentials = relationship("UserCredentials", uselist=False, back_populates="user")

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
