"""
This module contains tests for the user services.

Author: Yo
"""
# pylint: skip-file
from src.services.user_services import UserService, User, UserCredentials
from sqlalchemy.orm import Session

def tet_register_user(test_db_session: Session):
    """Test that a user is registered correctly."""
    user = UserService.register_user(test_db_session, "test_user", "testuser@gmail.com", "test_password")
    
    assert user is not None, "El usuario no se registró correctamente."
    assert user.user_id is not None, "El usuario no tiene un ID asignado."
    assert user.username == "test_user", "El nombre de usuario no coincide."

    credentials = test_db_session.query(UserCredentials).filter_by(user_id=user.user_id).first()

    assert credentials is not None, "Las credenciales del usuario no se registraron correctamente."
    assert credentials.email == "testuser@gmail.com", "El correo electrónico no coincide."

def test_login(test_db_session: Session):
    """Test that a user can log in correctly."""
    user = UserService.login_user(test_db_session, "testuser@gmail.com", "test_password")
    
    assert user is not None, "El usuario no pudo iniciar sesión."

    credentials = test_db_session.query(UserCredentials).filter_by(user_id=user.user_id).first()

    assert credentials is not None, "Las credenciales del usuario no se registraron correctamente."
    assert credentials.email == "testuser@gmail.com", "El correo electrónico no coincide."
    assert credentials.password_hash is not None, "La contraseña no coincide."

def tet_delete_user(test_db_session: Session):
    """Test that the user is deleted correctly."""
    user = test_db_session.query(User).filter_by(user_id=1).first()
    assert user is not None, "El usuario con ID 4 no existe antes de eliminarlo."
    
    UserService.delete_user(test_db_session, 1)
    
    user_deleted = test_db_session.query(User).filter_by(user_id=4).first()
    credentials_deleted = test_db_session.query(UserCredentials).filter_by(user_id=1).first()
    
    assert user_deleted is None, "El usuario no fue eliminado correctamente."
    assert credentials_deleted is None, "Las credenciales del usuario no fueron eliminadas correctamente."
