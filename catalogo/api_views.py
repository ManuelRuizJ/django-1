from django.db import models
from django.db.models import Q
from rest_framework import viewsets

from .models import Cancion, Playlist
from .serializers import CancionSerializers, PlaylistSerializers

class CancionViewSet(viewsets.ModelViewSet):
    queryset = Cancion.objects.all()
    serializer_class = CancionSerializers

    def get_queryset(self):
            canciones = Cancion.objects.all().prefetch_related("playlists")
            parametros = self.request.query_params
            q = parametros.get("q", "").strip()
            genero = parametros.get("genero", "").strip()
            artista = parametros.get("artista", "").strip()
    
            if q:
                canciones = canciones.filter(
                    Q(titulo__icontains=q) | Q(artista__icontains=q)
                )
    
            if genero:
                canciones = canciones.filter(playlists__genero=genero).distinct()
    
            if artista:
                canciones = canciones.filter(artista__iexact=artista)
    
            return canciones

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = (
        Playlist.objects.annotate(num_canciones=models.Count("canciones")).order_by("nombre")
    )
    serializer_class = PlaylistSerializers