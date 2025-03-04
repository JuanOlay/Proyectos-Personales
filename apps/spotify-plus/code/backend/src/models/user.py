""" 
Este módulo representa el modelo de usuario

Author: yo
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..databases import Base # pylint: disable=import-error

user_song_affinity = Table(
    "user_song_affinity",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.song_id"), primary_key=True),
    Column("affinity_level", Integer, nullable=False)  # Nivel de afinidad (1-5)
)


class User (Base):

    """This class represents the user model"""
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)

    credentials = relationship("UserCredentials", uselist=False, back_populates="user")
    created_songs = relationship('Song', back_populates='creator')
    created_playlists = relationship("Playlist", back_populates="creator")
    queue = relationship("Queue", back_populates="user", cascade="all, delete-orphan")
    song_affinities = relationship(
        "Song",
        secondary=user_song_affinity,
        back_populates="users_with_affinity"
        )
    history = relationship("History", back_populates="user")

    """
    def __init__(self, username: str, email: str, password: str):
        
        # Initializes the user model.
        #
        #Args:
        #    username (str): The username of the user.
        #    email (str): The email of the user.
        #    password (str): The password of the user (will be hashed).
        
        self.username = username
        self.credentials = UserCredentials(user_id=self, email=email, password=password)
    """

    def __repr__(self):
        """
        This method is used to represent the user model as a string
        """

        return f'<User {self.username}>'
