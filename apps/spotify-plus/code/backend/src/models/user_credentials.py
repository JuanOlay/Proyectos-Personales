"""
This module represents the user credentials model

Author: yo
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..databases import Base

class UserCredentials(Base):
    """
    This class represents the user credentials model
    """
    __tablename__ = "user_credentials"
    __table_args__ = {"extend_existing": True} # eliminar cuando se haga el main.py

    credentials_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    user = relationship("User", back_populates="credentials")

    def __repr__(self):
        """
        This method is used to represent the user credentials model as a string
        """
        return f"<UserCredentials {self.email}>"
