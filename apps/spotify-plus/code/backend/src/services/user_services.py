"""
This is the service module for the user entity.

Author: yomerito
"""
import logging
from sqlalchemy.orm import Session # pylint: disable=ungrouped-imports
from sqlalchemy.exc import SQLAlchemyError # pylint: disable=ungrouped-imports
from passlib.context import CryptContext
from ..models import User, UserCredentials

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class UserService:
    """
    This class represents the user service.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Compara una contraseña en texto plano con su hash almacenado.
        
        Args:
            plain_password (str): La contraseña en texto plano
            hashed_password (str): El hash de la contraseña
        """
        is_valid = UserService.pwd_context.verify(plain_password, hashed_password)

        return is_valid

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """
        Verifica si el usuario con el email dado tiene la contraseña correcta.
        
        Args:
            db (Session): La sesión de la base de datos
            email (str): El email del usuario
            password (str): La contraseña del usuario
        """
        user_credentials = db.query(UserCredentials).filter_by(email=email).first()
        if not user_credentials or not UserService.verify_password(
            password,
            user_credentials.password_hash
        ):
            raise ValueError("Credenciales inválidas")

        return user_credentials.user  # Se usa la relación entre `UserCredentials` y `User`

    @staticmethod
    def create_user(db: Session, username: str) -> User:
        """
        Crea un usuario en la base de datos sin credenciales.
        
        Args:
            db (Session): La sesión de la base de datos
            username (str): El nombre de usuario
        """
        existing_user = db.query(User).filter_by(username=username).first()
        if existing_user:
            raise ValueError("El usuario ya existe")

        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def create_user_credentials(
        db: Session,
        user_id: int,
        email: str,
        password: str
        ) -> UserCredentials:
        """
        Crea las credenciales de un usuario.
        
        Args:
            db (Session): La sesión de la base de datos
            user_id (int): El ID del usuario
            email (str): El email del usuario
            password (str): La contraseña del usuario
        """
        if db.query(UserCredentials).filter(UserCredentials.email == email).first():
            raise ValueError("El email ya está en uso")

        hashed_password = UserService.pwd_context.hash(password)
        credentials = UserCredentials(user_id=user_id, email=email, password_hash=hashed_password)
        db.add(credentials)
        db.commit()
        db.refresh(credentials)

        return credentials

    @staticmethod
    def register_user(db: Session, username: str, email: str, password: str) -> User:
        """
        Registra un usuario en la base de datos.
        
        Args:
            db (Session): La sesión de la base de datos
            username (str): El nombre de usuario
            email (str): El email del usuario
            password (str): La contraseña del usuario
        """
        user = UserService.create_user(db, username)
        UserService.create_user_credentials(db, user.user_id, email, password)

        return user

    # metodo provisional es necesario agregar una identificacion para que no
    # cualquier usuario pueda borrar cualquier otro usuario

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Elimina un usuario y sus credenciales de la base de datos.
        
        Args:
            db (Session): La sesión de la base de datos
            user_id (int): El ID del usuario a eliminar
        """
        try:
            credentials = db.query(UserCredentials).filter_by(user_id=user_id).first()
            if credentials:
                db.delete(credentials)

            user = db.query(User).filter_by(user_id=user_id).first()
            if user:
                db.delete(user)

            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logging.error("Error al eliminar el usuario %d: %s", user_id, e)
            return False

    @staticmethod
    def login_user(db: Session, email: str, password: str) -> User:
        """
        Autentica un usuario y devuelve su información si las credenciales son correctas.
        
        Args:
            db (Session): La sesión de la base de datos
            email (str): El email del usuario
            password (str): La contraseña del usuario
        """
        user = UserService.authenticate_user(db, email, password)
        return user
