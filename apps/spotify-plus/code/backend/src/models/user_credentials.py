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
    __table_args__ = {"extend_existing": True} # eliminar cuando se haga el main.py

    credentials_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)  # Corregido
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    user = relationship("User", back_populates="credentials")

    """
    def __init__(self, user_id: int, email: str, password: str):
        
        # This method is used to initialize the user credentials model
        #
        # Args:
        #    user_id (int): The ID of the user
        #    email (str): The email of the user
        #    password (str): The password of the user


        self.user_id = user_id
        self.email = email
        self.password_hash = generate_password_hash(password)
    """

    def __repr__(self):
        """
        This method is used to represent the user credentials model as a string
        """
        return f"<UserCredentials {self.email}>"
