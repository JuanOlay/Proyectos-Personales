"""Módulo para la configuración de la base de datos con SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"  # Cambia esto por tu URL de base de datos

engine = create_engine(DATABASE_URL, echo=True)  # echo=True para ver las consultas SQL en consola
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    """
    Función para obtener una sesión de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
