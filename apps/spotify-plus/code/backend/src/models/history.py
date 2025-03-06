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
    __table_args__ = {'extend_existing': True} # eliminar cuando se haga el main.py

    history_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.song_id"), nullable=False)
    played_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="history")
    song = relationship("Song", back_populates="history")

    def __repr__(self):
        """
        Returns the string representation of the History model
        """
        return f'<History {self.history_id}>'
