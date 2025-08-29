# pylint: skip-file
from sqlalchemy.orm import Session
from src.services.queue_services import QueueService, Queue, queue_song_association
from src.services.song_services import Song
import logging
import time


def tet_add_song_to_queue(test_db_session: Session):
    
    song = test_db_session.query(Song).filter_by(song_id=1).first()

    QueueService.delete_queue(test_db_session, 1)
    
    queue = QueueService.add_song_to_queue(test_db_session, 1, 1)
    QueueService.add_song_to_queue(test_db_session, 1, 2)
    QueueService.add_song_to_queue(test_db_session, 1, 3)
    QueueService.add_song_to_queue(test_db_session, 1, 4)
    QueueService.add_song_to_queue(test_db_session, 1, 5)
    QueueService.add_song_to_queue(test_db_session, 1, 6)
    QueueService.add_song_to_queue(test_db_session, 1, 7)
    QueueService.add_song_to_queue(test_db_session, 1, 8)
    QueueService.add_song_to_queue(test_db_session, 1, 9)
    QueueService.add_song_to_queue(test_db_session, 1, 10)
    assert queue is not None, "La canción no se agregó a la cola correctamente."
    assert song in queue.queue_songs, "La canción no está en la cola."

def tet_delete_queue(test_db_session: Session):
    queue = test_db_session.query(Queue).filter_by(queue_id=1).first()
    assert queue is not None, "La cola con ID 1 no existe antes de eliminarla."

    QueueService.delete_queue(test_db_session, 1)

    queue_after = test_db_session.query(Queue).filter_by(queue_id=1).first()
    assert queue_after is None, "La cola no se eliminó correctamente."

def tet_remove_song_from_queue(test_db_session: Session):
    queue = test_db_session.query(Queue).filter_by(queue_id=1).first()
    assert queue is not None, "La cola con ID 1 no existe."

    canciones_antes = list(queue.queue_songs)  # Guardamos el estado antes de eliminar

    QueueService.remove_song_from_queue(test_db_session, 1, 3)

def tet_get_queue(test_db_session: Session):
    songs = QueueService.get_queue_songs(test_db_session, 1)

    assert songs is not None, "No se encontraron canciones para la cola con ID 1."

    # Imprimir log de las canciones
    for song in songs:
        logging.info(f"Song ID: {song.song_id}, Title: {song.song_title}, Artist: {song.artist}")

    assert isinstance(songs, list), "El resultado debe ser una lista de canciones."
    assert len(songs) > 0, "La cola no tiene canciones asociadas."

def tet_view_queue(test_db_session: Session):
    queue = QueueService.view_songs_queue(test_db_session, 1)
    assert queue is not None, "No se encontró la cola con ID 1."

def tet_next_song(test_db_session: Session):
    # Avanza a la siguiente canción a partir de la posición 8
    next_song_assoc = QueueService.next_song(test_db_session, queue_id=1, position=1)
    # Se podría usar un sleep corto para simular el tiempo de reproducción
    time.sleep(10)  # Nota: en tests unitarios es preferible evitar sleep y usar mocks
    
    # Obtener la cola actualizada para verificar el puntero current_song_id
    queue = test_db_session.query(Queue).filter(Queue.queue_id == 1).first()
    assert queue is not None, "La cola no existe."
    assert queue.current_song_id is not None, "El puntero current_song_id no se actualizó."
    
    # Avanzar a la siguiente canción usando el current_song_id obtenido
    new_song_assoc = QueueService.next_song(test_db_session, queue_id=1, position=queue.current_song_id)
    time.sleep(10)
    
    # Verificar que se haya avanzado correctamente
    assert new_song_assoc is not None, "No se encontró la siguiente canción en la cola."
    logging.info("Test de next_song exitoso. Current_song_id actualizado: %s", queue.current_song_id)

def tet_prev_song(test_db_session: Session):
    song = QueueService.previous_song(test_db_session, 1 ,1)
    time.sleep(20)
    QueueService.previous_song(test_db_session, 1)
    time.sleep(10)
    assert song is not None, "No se encontró la canción anterior en la cola."

def tet_next_and_prev(test_db_session: Session):
    song = QueueService.next_song(test_db_session, 1, 5)
    time.sleep(20)
    QueueService.next_song(test_db_session, 1)
    time.sleep(10)
    assert song is not None, "No se encontró la siguiente canción en la cola."

    song = QueueService.previous_song(test_db_session, 1)
    time.sleep(20)
    QueueService.previous_song(test_db_session, 1)
    time.sleep(10)
    assert song is not None, "No se encontró la canción anterior en la cola"