from rest_framework import serializers
from .models import Cancion, Playlist

class PlaylistResumenSeriizers(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["id", "nombre", "genero"]


class PlaylistSerializers(serializers.ModelSerializer):
    num_canciones = serializers.IntegerField(read_only=True)

    class Meta:
        model = Playlist
        fields = ["id", "playlist_id", "nombre", "genero", "num_canciones"]


class CancionSerializers(serializers.ModelSerializer):
    # Lectura --> Las playlists anidadas con nombre y género
    playlists = PlaylistResumenSeriizers(many=True, read_only=True)

    # Escritura --> Cuando el cliente manda solo los IDs de las playlists
    playlist_ids = serializers.PrimaryKeyRelatedField(
        source="playlists",
        queryset=Playlist.objects.all(),
        many=True,
        write_only=True,
        required=True,
    )

    class Meta:
        model = Cancion
        fields = [
            "spotify_id",
            "titulo",
            "artista",
            "album",
            "popularidad",
            "duracion_ms",
            "fecha_lanzamiento",
            "creada_en",
            "playlists",     # Usado para la LECTURA (devuelve el objeto anidado)
            "playlist_ids",  # Usado para la ESCRITURA (recibe los IDs)
        ]
        read_only_fields = ["creada_en"]

    def validate_popularidad(self, valor):
        if valor > 100 or valor < 0:
            raise serializers.ValidationError("La popularidad va de 0 a 100")
        return valor