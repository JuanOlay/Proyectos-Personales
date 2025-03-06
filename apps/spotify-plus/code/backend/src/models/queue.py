"""
This is the Queue model. It is used to store the queue of songs that are to be played.

Author: yo"""
from sqlalchemy import Column, Integer, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from ..databases import Base

# tabla intermedia para la relación muchos a muchos entre Queue y Song
queue_song_association = Table(
    'queue_song_association',
    Base.metadata,
    Column('queue_id', Integer, ForeignKey('queue.queue_id')),
    Column('song_id', Integer, ForeignKey('songs.song_id')),
    Column('position', Integer)
)

class Queue(Base):
    """Queue model"""
    __tablename__ = 'queue'
    __table_args__ = {'extend_existing': True}

    queue_id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
        ) # user_id es requerido por ahora
    playlist_id = Column(Integer, ForeignKey("playlists.playlist_id"), nullable=True)
    current_song_id = Column(Integer, ForeignKey("songs.song_id"), nullable=True)

    repeat = Column(Boolean, default=False)
    shuffle = Column(Boolean, default=False)

    user = relationship("User", back_populates="queue")
    playlist = relationship("Playlist", back_populates="queue")
    current_song = relationship("Song", foreign_keys=[current_song_id])
    queue_songs = relationship("Song", secondary=queue_song_association, back_populates="in_queues")

    def __repr__(self):
        """
        Returns the string representation of the Queue model
        """
        return f'<Queue {self.queue_id}>'
