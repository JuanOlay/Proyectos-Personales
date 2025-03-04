"""Configuración de pruebas para pytest"""
# pylint: skip-file

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.databases import Base  # Importamos Base para crear las tablas

# Configuración de la base de datos de prueba
TEST_DB_URL = "sqlite:///tests/test_db.sqlite"  # Guarda la base de datos en un archivo

@pytest.fixture(scope="session")
def test_engine():
    # Crea el motor de la base de datos de prueba.
    engine = create_engine(TEST_DB_URL, echo=True)  # Puedes quitar `echo=True` si no quieres logs
    Base.metadata.create_all(engine)  # Crea las tablas en la BD de prueba
    yield engine
    engine.dispose()  # Cierra la conexión después de las pruebas


@pytest.fixture(scope="function")
def test_db_session(test_engine):
    # Crea una sesión de base de datos para cada prueba
    TestingSessionLocal = sessionmaker(bind=test_engine)
    session = TestingSessionLocal()



    yield session  # Devuelve la sesión de prueba
    session.close()

"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.databases import Base  # Importamos Base para crear las tablas

# Configuración de la base de datos de prueba
TEST_DB_URL = "sqlite:///:memory:"  # O usa "sqlite:///:memory:" para que sea en RAM

@pytest.fixture(scope="session")
def test_engine():
    #Crea el motor de la base de datos de prueba.
    engine = create_engine(TEST_DB_URL, echo=True)  # Puedes quitar `echo=True` si no quieres logs
    Base.metadata.create_all(engine)  # Crea las tablas en la BD de prueba
    yield engine
    engine.dispose()  # Cierra la conexión después de las pruebas


@pytest.fixture(scope="function")
def test_db_session(test_engine):
    # Crea una sesión de base de datos para cada prueba
    TestingSessionLocal = sessionmaker(bind=test_engine)
    session = TestingSessionLocal()

    # Elimina y vuelve a crear todas las tablas para cada prueba
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)

    yield session  # Devuelve la sesión de prueba
    session.rollback()  # Revierte cambios después de cada prueba
    session.close()
"""