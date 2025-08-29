"""
This is the queue service.

Author: yomerito
"""
import logging
from typing import Optional
from sqlalchemy import delete, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from ..models.queue import Queue, queue_song_association
from ..models.song import Song
from .song_services import SongService

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class QueueService:
    """
    This class represents the queue service.
    """
    @staticmethod
    def create_queue(db: Session, user_id: int):
        """
        Crea una nueva cola de reproducción para el usuario si no existe.
        
        Args:
            db (Session): La sesión de la base de datos.
            user_id (int): El ID del usuario propietario de la cola.
        """
        try:
            new_queue = Queue(user_id=user_id)
            db.add(new_queue)
            db.commit()
            logging.info("Cola de reproducción creada correctamente.")
            return new_queue
        except SQLAlchemyError as e:
            db.rollback()
            logging.error("Error al crear la cola de reproducción: %s", e)
            return None

    @staticmethod
    def get_max_position(db: Session, queue_id: int) -> int:
        """
        Obtiene la posición más alta en la cola especificada.
        
        Args:
            db (Session): La sesión de la base de datos.
            queue_id (int): El ID de la cola de reproducción.
        """
        max_position = db.query(
            func.max(
                queue_song_association.c.position
                )
            ).filter_by(queue_id=queue_id).scalar()
        return max_position if max_position is not None else 0

    @staticmethod
    def is_valid_position(db: Session, queue_id: int, position: int) -> bool:
        """
        Verifica si la posición es válida en la cola.
        
        Args:
            db (Session): La sesión de la base de datos.
            queue_id (int): El ID de la cola de reproducción.
            position (int): La posición a verificar.
        """
        max_position = QueueService.get_max_position(db, queue_id)
        return position <= max_position + 1

    @staticmethod
    def assign_position_automatically(db: Session, queue_id: int, position: Optional[int]) -> int:
        """
        Asigna automáticamente una posición si no se proporciona.
        
        Args:
            db (Session): La sesión de la base de datos.
            queue_id (int): El ID de la cola de reproducción.
            position (Optional[int]): La posición deseada.
        """
        if position is None:
            return QueueService.get_max_position(db, queue_id) + 1
        return position

    @staticmethod
    def shift_songs_forward(db: Session, queue_id: int, position: int):
        """
        Desplaza todas las canciones desde la posición dada una posición adelante.

        Args:
            db (Session): La sesión de la base de datos.
            queue_id (int): El ID de la cola de reproducción.
            position (int): La posición a partir de la cual se desplazarán las canciones.
        """
        try:
            update_stmt = (
                update(queue_song_association)
                .where(
                    (queue_song_association.c.queue_id == queue_id) &
                    (queue_song_association.c.position >= position)
                )
                .values(position=queue_song_association.c.position + 1)
            )

            db.execute(update_stmt)
            logging.info(
                "Se desplazaron las canciones en la cola %d desde la posición %d",
                queue_id,
                position
            )

        except SQLAlchemyError as e:
            logging.error(
                "Error al desplazar canciones en la cola %d desde la posición %d: %s",
                queue_id,
                position,
                e
            )

    @staticmethod
    def shift_songs_backward(db: Session, queue_id: int, position: int):
        """
        Desplaza todas las canciones desde la posición dada una posición hacia atrás.
        
        Args:
            db (Session): La sesión de la base de datos.
            queue_id (int): El ID de la cola de reproducción.
            position (int): La posición a partir de la cual se desplazarán las canciones.
        """
        try:
            update_stmt = (
                update(queue_song_association)
                .where(
                    (queue_song_association.c.queue_id == queue_id) &
                    (queue_song_association.c.position > position)
                    # Solo mover las canciones que están después de la posición eliminada
                )
                .values(position=queue_song_association.c.position - 1)
            )

            db.execute(update_stmt)
            db.commit()
            logging.info(
                "Se desplazaron las canciones en la cola %d desde la posición %d hacia atrás.",
                queue_id,
                position
            )
        except SQLAlchemyError as e:
            db.rollback()
            logging.error(
                "Error al desplazar canciones en la cola %d desde la posición %d: %s",
                queue_id,
                position,
                e
            )

    @staticmethod
    def add_song_to_queue(
        db: Session,
        queue_id: int,
        song_id: int,
        position: Optional[int] = None
        ):
        """
        Agrega una canción a la cola de reproducción en una posición específica.
        Si la posición ya está ocupada, desplaza las canciones existentes hacia adelante.
        No permite asignar posiciones mayores a (posición máxima + 1).
        
        Args:
            db (Session): La sesión de la base de datos.
            queue_id (int): El ID de la cola de reproducción.
            song_id (int): El ID de la canción a agregar.
            position (Optional[int]): La posición deseada
        """
        try:
            # Verificar si la cola existe
            queue = db.query(Queue).filter(Queue.queue_id == queue_id).first()
            if not queue:
                logging.info("Queue con ID %d no encontrada. Creando una nueva...")
                queue = QueueService.create_queue(db, user_id=1)
                if not queue:
                    return None

            # Verificar si la canción existe
            song = db.query(Song).filter(Song.song_id == song_id).first()
            if not song:
                logging.error("Canción con ID %d no encontrada.", song_id)
                return None

            # Asignar posición automáticamente si no se proporciona
            position = QueueService.assign_position_automatically(db, queue_id, position)

            # Verificar si la posición es válida
            if not QueueService.is_valid_position(db, queue_id, position):
                logging.error("Posición inválida: %d. La posición máxima permitida es %d.",
                            position, QueueService.get_max_position(db, queue_id) + 1)
                return None

            # Mover canciones si la posición ya está ocupada
            QueueService.shift_songs_forward(db, queue_id, position)

            # Insertar la nueva canción en la posición deseada
            insert_stmt = queue_song_association.insert().values(
                queue_id=queue_id,
                song_id=song_id,
                position=position
            )
            db.execute(insert_stmt)
            db.commit()

            logging.info(
                "Canción con ID %d" +
                " agregada a la cola con ID %d en la posición %d, desplazando las demás.",
                song_id, queue_id, position
            )
            return queue

        except SQLAlchemyError as e:
            db.rollback()
            logging.error("Error al agregar canción a la cola: %s", e)
            return None

    @staticmethod
    def remove_song_from_queue(db: Session, queue_id: int, position: int):
        """
        Elimina una canción de la cola de reproducción en la posición dada.
        
        Args:
            db (Session): La sesión de la base de datos.
            queue_id (int): El ID de la cola de reproducción.
            position (int): La posición de la canción a eliminar
        """
        try:
            queue = db.query(Queue).filter(Queue.queue_id == queue_id).first()
            if not queue:
                logging.error("Queue con ID %d no encontrada.", queue_id)
                return None

            # Verificar que la canción existe antes de intentar moverla
            song_to_remove = db.query(queue_song_association).filter(
                queue_song_association.c.queue_id == queue_id,
                queue_song_association.c.position == position
            ).first()

            if not song_to_remove:
                logging.error("No se encontró canción en la posición %d.", position)
                return None

            # Eliminar la canción en la posición dada
            remove_stmt = delete(queue_song_association).where(
                (queue_song_association.c.queue_id == queue_id) &
                (queue_song_association.c.position == position)
            )
            db.execute(remove_stmt)
            db.commit()
            logging.info("Canción eliminada de la cola en la posición %d", position)

            # Ahora que la canción ha sido eliminada, mover las canciones posteriores hacia atrás
            QueueService.shift_songs_backward(db, queue_id, position)

            # Forzar la actualización de la relación
            queue = db.query(Queue).filter_by(queue_id=queue_id).first()
            db.expire(queue, ['queue_songs'])

            return queue

        except SQLAlchemyError as e:
            db.rollback()
            logging.error("Error al eliminar canción de la cola: %s", e)
            return None

    @staticmethod
    def get_queue_songs(db: Session, queue_id: int):
        """
        Obtiene las canciones en la cola de reproducción.
        
        Args:
            db (Session): La sesión de la base de datos.
            queue_id (int): El ID de la cola de reproducción.
        """
        try:
            # Consultar las canciones asociadas a la cola a través de la tabla de asociación
            songs = db.query(Song).join(
                queue_song_association
            ).filter(
                queue_song_association.c.queue_id == queue_id
            ).all()

            if not songs:
                logging.error("No se encontraron canciones para la cola con ID %d.", queue_id)
                return None

            return songs
        except SQLAlchemyError as e:
            logging.error("Error al obtener canciones de la cola: %s", e)
            return None

    @staticmethod
    def view_songs_queue(db: Session, queue_id: int):
        """
        Muestra las canciones en la cola de reproducción.
        
        Args:
            db (Session): La sesión de la base de datos.
            queue_id (int): El ID de la cola de reproducción.
        """
        query = db.query(
            queue_song_association.c.song_id,
            Song.__table__.c.song_title,
            Song.__table__.c.artist
        ).join(
            Song.__table__,
            Song.__table__.c.song_id == queue_song_association.c.song_id
        ).filter(
            queue_song_association.c.queue_id == queue_id
        )
        results = query.all()  # Obtenemos todas las filas

        # Imprime en consola
        for row in results:
            print(f"Song ID: {row.song_id}, Title: {row.song_title}, Artist: {row.artist}")

        # Devolvemos la lista de resultados para que el test no sea None
        return results

    @staticmethod
    def update_current_song(db: Session, queue: Queue, position: int):
        """
        Actualiza el puntero current_song_id a la posición en la cola de la siguiente canción,
        tras haberse removido la canción anterior.
        
        Args:
            db (Session): La sesión de la base de datos.
            queue (Queue): La cola de reproducción actual.
            position (int): La posición que ocupará la siguiente canción.
        
        Returns:
            La asociación de la siguiente canción si existe, o None en caso contrario.
        """
        # Se busca la canción que ahora se encuentre en 'position'
        next_song_assoc = db.query(queue_song_association).filter(
            queue_song_association.c.queue_id == queue.queue_id,
            queue_song_association.c.position == position
        ).first()

        if next_song_assoc:
            # Aquí se asigna la posición en la cola, no la ID de la canción
            queue.current_song_id = position
            db.commit()  # Guardamos la actualización en la base de datos
            return next_song_assoc
        else:
            # No hay canción en esa posición (cola vacía o fin de la cola)
            return None

    @staticmethod
    def next_song(db: Session, queue_id: int, position: Optional[int] = None):
        """
        Avanza a la siguiente canción en la cola.
        Se determina la posición actual (si no se indica, se asume la posición 1),
        se remueve la canción actual y se actualiza el puntero current_song_id con la posición
        en la que se encuentra la siguiente canción, para luego reproducirla.
        
        Args:
            db (Session): La sesión de la base de datos.
            queue_id (int): El ID de la cola de reproducción.
            position (Optional[int]): La posición de la canción actual. Si no se especifica, se asume 1.
        
        Returns:
            La asociación de la siguiente canción si existe, o None en caso de error o si no hay siguiente canción.
        """
        try:
            # Obtener la cola
            queue = db.query(Queue).filter(Queue.queue_id == queue_id).first()
            if not queue:
                logging.error("Queue con ID %d no encontrada.", queue_id)
                return None

            # Si no se especifica posición, asumimos que la canción actual está en la posición 1.
            if position is None:
                position = 1

            # Remover la canción actual de la cola en la posición indicada
            updated_queue = QueueService.remove_song_from_queue(db, queue_id, position)
            if updated_queue is None:
                logging.error("Error al remover la canción en la posición %d de la cola %d.", position, queue_id)
                return None

            # Actualizar el puntero current_song_id a la posición de la siguiente canción
            next_song_assoc = QueueService.update_current_song(db, updated_queue, position)
            if next_song_assoc is None:
                logging.info("No hay siguiente canción en la cola para reproducir.")
                return None

            # Reproducir la nueva canción actual usando el servicio de canciones
            SongService.play_song(db, next_song_assoc.song_id)

            logging.info("Se avanzó a la siguiente canción, se actualizó current_song (posición: %d) y se inició la reproducción.", position)
            return next_song_assoc

        except SQLAlchemyError as e:
            db.rollback()
            logging.error("Error al avanzar a la siguiente canción: %s", e)
            return None



    @staticmethod
    def previous_song(db: Session, queue_id: int, position: Optional[int] = None):
        """
        Retrocede a la canción anterior en la cola de reproducción y la reproduce.
        Permite especificar la posición actual (opcional; por defecto se asume la posición 1).
        Se verifica que exista una canción anterior (la posición actual no debe ser la primera).
        Si existe, se elimina la canción en la posición actual y se reproduce la canción anterior.
        """
        try:
            if position is None:
                position = 1

            # Verificar que la cola exista
            queue = db.query(Queue).filter(Queue.queue_id == queue_id).first()
            if not queue:
                logging.error("Queue con ID %d no encontrada.", queue_id)
                return None

            # Verificar que haya una canción en la posición actual
            current_song_assoc = db.query(queue_song_association).filter(
                queue_song_association.c.queue_id == queue_id,
                queue_song_association.c.position == position
            ).first()
            if not current_song_assoc:
                logging.info(
                    "No hay canción en la posición %d de la cola con ID %d.",
                    position,
                    queue_id
                    )
                return None

            # Si la posición es la primera, no existe canción anterior para retroceder
            if position == 1:
                logging.info(
                    "La posición %d es la primera en la cola." +
                    "No hay canción anterior para reproducir.",
                    position
                    )
                return None

            # Verificar si existe una canción anterior (la que estaría en la posición anterior)
            previous_song_candidate = db.query(queue_song_association).filter(
                queue_song_association.c.queue_id == queue_id,
                queue_song_association.c.position == position - 1
            ).first()
            if not previous_song_candidate:
                logging.info("No se encontró canción anterior en la posición %d.", position - 1)
                return None

            # Eliminar la canción actual en la posición especificada y
            # reajustar posiciones posteriores
            QueueService.remove_song_from_queue(db, queue_id, position)

            # La canción anterior permanece en la misma posición (position - 1)
            previous_song_assoc = db.query(queue_song_association).filter(
                queue_song_association.c.queue_id == queue_id,
                queue_song_association.c.position == position - 1
            ).first()
            if not previous_song_assoc:
                logging.info(
                    "No se encontró la canción anterior en la posición %d " +
                    "después de eliminar la canción actual.",
                position - 1
                )
                return None

            # Reproducir la canción anterior usando el servicio de canciones
            SongService.play_song(db, previous_song_assoc.song_id)
            logging.info(
                "Reproduciendo canción anterior en la cola %d desde la posición %d: canción ID %d",
                queue_id, position - 1, previous_song_assoc.song_id
            )
            return previous_song_assoc

        except SQLAlchemyError as e:
            db.rollback()
            logging.error(
                "Error al retroceder a la canción anterior desde la posición %d: %s",
                position,
                e
            )
            return None


    # se podria reemplazar por un clear queue pero por el momento se
    # considera mejor eliminar toda la queue en vez de eliminarla y volverla a crear

    @staticmethod
    def delete_queue(db: Session, queue_id: int):
        """
        Elimina la cola de reproducción.
        """
        try:
            queue = db.query(Queue).filter(Queue.queue_id == queue_id).first()

            if not queue:
                logging.error("Queue con ID %d no encontrada.", queue_id)
                return None
            db.query(queue_song_association).filter_by(queue_id=1).delete()
            db.commit()
            db.delete(queue)
            db.commit()
            logging.info("Queue con ID %d eliminada correctamente.", queue_id)
            return queue
        except SQLAlchemyError as e:
            db.rollback()
            logging.error("Error al eliminar la cola: %s", e)
            return None
