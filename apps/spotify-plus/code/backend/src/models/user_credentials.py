"""
This module represents the user credentials model

Author: yo
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..databases import Base # pylint: disable=import-error

class UserCredentials(Base):
    """
    This class represents the user credentials model
    """
    __tablename__ = "user_credentials"
    __table_args__ = {'extend_existing': True}  # Permite redefinir la tabla

    credentials_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    user = relationship("User", back_populates="credentials")

    def __init__(self, user_id: int, email: str, password: str):
        """
        This method is used to initialize the user credentials model
        """
        self.user_id = user_id
        self.email = email
        self.password = password

    def __repr__(self):
        """
        This method is used to represent the user credentials model as a string
        """
        return f"<UserCredentials {self.email}>"
