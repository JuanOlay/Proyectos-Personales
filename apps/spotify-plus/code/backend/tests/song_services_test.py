# pylint: skip-file
from sqlalchemy.orm import Session
from src.services.song_services import SongService,Song
import os
import time
from src.services.user_services import User

def tet_add_song(test_db_session: Session):
    test_user = test_db_session.query(User).filter_by(user_id=1).first()
    assert test_user is not None, "El usuario de prueba no existe."

    file_path = "tests/Snails_House_-_Hot_Milk_.mp3"
    print(f"Verificando archivo en: {os.path.abspath(file_path)}")
    print(f"Existe: {os.path.exists(file_path)}")
    
    assert os.path.exists(file_path), f"El archivo {file_path} no existe."
    
    song = SongService.add_song(
        test_db_session,
        file_path,
        "Hot Milk",
        "Snails House",
        1,
        test_user
    )
    
    assert song is not None, "La canción no se agregó correctamente."
    assert song.song_id is not None, "La canción no tiene un ID asignado."
    assert song.song_title == "Hot Milk", "El título de la canción no coincide."
    assert song.artist == "Snails House", "El artista de la canción no coincide."

def tet_play_song(test_db_session: Session):
    """Reproduce la canción."""
    song = test_db_session.query(Song).filter_by(song_id=1).first()
    assert song is not None, "La canción con ID 1 no existe."
    
    result = SongService.play_song(test_db_session, 1)
    assert result is True, "No se pudo reproducir la canción."

def tet_delete_song(test_db_session: Session):
    """Elimina la canción."""
    song = test_db_session.query(Song).filter_by(song_id=1).first()
    assert song is not None, "La canción con ID 2 no existe antes de eliminarla."
    
    SongService.delete_song(test_db_session, 1)
    
    song_after = test_db_session.query(Song).filter_by(song_id=1).first()
    assert song_after is None, "La canción no se eliminó correctamente."

def tet_pause_and_unpause_song(test_db_session: Session):
    """Pausa y reanuda la canción."""
    song = test_db_session.query(Song).filter_by(song_id=1).first()
    assert song is not None, "La canción con ID 1 no existe."
    
    result_play = SongService.play_song(test_db_session, 1)
    
    time.sleep(10)
    result_pause = SongService.pause_song()
    
    time.sleep(5)
    result_resume = SongService.play_song(test_db_session, 1)
    
    time.sleep(10)
