# pylint: skip-file
from sqlalchemy.orm import Session
from src.services.song_services import SongService, Song
import os

def tet_add_song(test_db_session: Session):
    file_path = "tests/Snails_House_-_Hot_Milk_.mp3"
    print(f"Verificando archivo en: {os.path.abspath(file_path)}")
    print(f"Existe: {os.path.exists(file_path)}")
    song = SongService.add_song(
        test_db_session,
        "tests/Snails_House_-_Hot_Milk_.mp3",
        "Snails House",
        "Hot Milk",
        1,
        1
    )
def test_play_song(test_db_session: Session):
    """Reproduce la canción."""
    SongService.play_song(test_db_session, 1)

def tet_delete_song(test_db_session: Session):
    """Elimina la canción."""
    SongService.delete_song(test_db_session, 1)
