"""
This is the history model. It is used to store the history of songs played by the user.

Author: yo
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime # pylint: disable=wrong-import-order
from ..databases import Base

class History(Base):
    """
    This class represents the history model
    """
    __tablename__ = 'history'
    __table_args__ = {'extend_existing': True}

    history_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    song_id = Column(Integer, ForeignKey("songs.song_id"))
    played_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="history")
    song = relationship("Song", back_populates="history")

    """
    def __init__(self, user_id, song_id):
        
        # Constructor for the History model
        #
        # Args:
        #     user_id (int): The id of the user who played the song
        #     song_id (int): The id of the song that was played
        #

        self.user_id = user_id
        self.song_id = song_id
        self.played_at = datetime.now()
    """

    def __repr__(self):
        """
        Returns the string representation of the History model
        """
        return f'<History {self.history_id}>'
