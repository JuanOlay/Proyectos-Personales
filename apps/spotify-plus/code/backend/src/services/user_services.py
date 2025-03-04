"""
This module contains the services for the user model.

Author: Yo"""
from sqlalchemy.orm import Session
from ..models import User, UserCredentials # pylint: disable=import-error
from ..databases import * # pylint: disable=import-error

class UserService:
    """
    This class represents the user service.
    """
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str) -> User:
        """
        Creates a new user.
        Args:
            db (Session): The database session
            username (str): The username of the user
            email (str): The email of the user
            password (str): The password of the user
        Returns:
            User: The created user
        """
        if db.query(UserCredentials).filter(UserCredentials.email == email).first():
            raise ValueError("Email already exists")

        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)

        credentials = UserCredentials(user_id=user.user_id, email=email, password_hash=password)
        db.add(credentials)
        db.commit()
        db.refresh(credentials)

        return user
