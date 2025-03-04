"""
This module contains the authentication service.
"""
from sqlalchemy.orm import Session
from ..models import User, UserCredentials # pylint: disable=import-error

class AuthenticationService:
    """
    This class represents the authentication service.
    """
    @staticmethod
    def register_user(db: Session, username: str, email: str, password: str) -> User:
        """
        Registers a new user.
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

        credentials = UserCredentials(user_id=user.id, email=email, password=password)
        db.add(credentials)
        db.commit()
        db.refresh(credentials)

        return user

    @staticmethod
    def login(db: Session, email: str, password: str) -> User:
        """
        Logs in a user.
        Args:
            db (Session): The database session
            email (str): The email of the user
            password (str): The password of the user
        Returns:
            User: The authenticated user
        """
        credentials = db.query(UserCredentials).filter(UserCredentials.email == email).first()
        if not credentials or credentials.password != password:
            raise ValueError("Invalid email or password")

        return credentials.user

    @staticmethod
    def logout(user: User):
        """
        Logs out a user.
        Args:
            user (User): The user to log out
        """
        print(f"User {user.username} has logged out.")
