"""
This module contains tests for the user services.

Author: Yo
"""
# pylint: skip-file
import pytest
from sqlalchemy.exc import IntegrityError
from src.services.user_services import UserService, User, UserCredentials
from sqlalchemy.orm import Session

def tet_register_user(test_db_session: Session):
    """Test that a user is registered correctly."""
    user = UserService.register_user(test_db_session, "test_user", "testuser@gmail.com", "test_password")

def tet_login(test_db_session: Session):
    """Test that a user can log in correctly."""
    user = UserService.login_user(test_db_session, "testuser@gmail.com", "test_password")

def tet_delete_user(test_db_session: Session):
    """Test that the user is deleted correctly."""
    UserService.delete_user(test_db_session, 4)

    # 4. Verificar que el usuario y sus credenciales ya no existen
    user_deleted = test_db_session.query(User).filter_by(user_id=4).first()
    credentials_deleted = test_db_session.query(UserCredentials).filter_by(user_id=4).first()