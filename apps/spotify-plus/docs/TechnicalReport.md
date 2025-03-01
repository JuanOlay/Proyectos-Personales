# User stories

## 🎵 Subida y Gestión de Canciones

### ID: SONG-001
**Título:** Subir una canción al sistema  
**Descripción:** Como usuario, quiero poder subir una canción con su información (título, artista, género, etc.), para que otros usuarios puedan escucharla.  
**Criterios de Aceptación:**  
- El usuario debe proporcionar el archivo de audio y los metadatos.  
- Solo el usuario que subió la canción o un administrador puede eliminarla.  
- La canción debe estar disponible en el catálogo tras su aprobación.  

### ID: SONG-002
**Título:** Eliminar una canción  
**Descripción:** Como usuario, quiero poder eliminar una canción que he subido, para gestionar mi contenido.  
**Criterios de Aceptación:**  
- Solo el usuario que subió la canción o un administrador puede eliminarla.  
- La canción eliminada debe desaparecer de todas las playlists donde estaba.  

## 🎧 Escucha y Recomendaciones

### ID: PLAY-001
**Título:** Escuchar una canción  
**Descripción:** Como usuario, quiero poder reproducir una canción desde la plataforma, para disfrutar del contenido disponible.  
**Criterios de Aceptación:**  
- La canción debe reproducirse sin errores.  
- Se debe registrar en el historial de canciones escuchadas.  

### ID: RECO-001
**Título:** Recibir recomendaciones de canciones  
**Descripción:** Como usuario, quiero recibir recomendaciones basadas en mi historial y nivel de afinidad con otras canciones, para descubrir nueva música.  
**Criterios de Aceptación:**  
- Las recomendaciones deben basarse en canciones que el usuario ha escuchado y su nivel de afinidad.  
- El usuario puede marcar una recomendación como "Me gusta" o "No me gusta" para mejorar el sistema.  

## 🎚 Gestión de Playlists y Afinidad

### ID: PL-001
**Título:** Ajustar la frecuencia de repetición de canciones en una playlist  
**Descripción:** Como usuario, quiero ajustar la frecuencia con la que aparece una canción en mi playlist, según mi nivel de afinidad con ella.  
**Criterios de Aceptación:**  
- El usuario puede establecer un nivel de afinidad del 1 al 10.  
- Las canciones con mayor afinidad deben repetirse con más frecuencia.  
- El ajuste debe reflejarse en la reproducción de la playlist.  

### ID: PL-002
**Título:** Filtrar canciones en una playlist  
**Descripción:** Como usuario, quiero poder filtrar las canciones de mi playlist por nombre, artista y favoritos, para encontrar la música que deseo escuchar.  
**Criterios de Aceptación:**  
- El usuario puede buscar por nombre de canción, artista o favoritos exclusivos de la playlist.  
- Los resultados deben actualizarse dinámicamente al escribir.  

## 🔹 Convención usada en los IDs

- **SONG-*** → Relacionado con la gestión de canciones.  
- **PLAY-*** → Relacionado con la reproducción de canciones.  
- **RECO-*** → Relacionado con recomendaciones.  
- **PL-*** → Relacionado con playlists.
