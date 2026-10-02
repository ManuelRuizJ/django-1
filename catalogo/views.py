# catalogo/views.py (reemplaza el contenido completo del archivo)
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from .models import Cancion, Playlist


def lista_canciones(request):
    q = request.GET.get("q", "").strip()
    genero = request.GET.get("genero", "").strip()

    canciones = Cancion.objects.all()

    if q:
        canciones = canciones.filter(
            Q(titulo__icontains=q) |
            Q(artista__icontains=q)
        )

    if genero:
            canciones = canciones.filter(
                 playlists__genero=genero
            )

    paginator = Paginator(canciones, 25)
    page_obj = paginator.get_page(request.GET.get("page"))

    contexto = {
        "page_obj": page_obj,
        "total": canciones.count(),
        "q": q,
        "genero": genero,
    }

    return render(request, "catalogo/lista.html", contexto)


def detalle_cancion(request, pk):
    cancion = get_object_or_404(Cancion, pk=pk)

    return render(request, "catalogo/detalle.html", {"cancion": cancion})


def detalle_playlist(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)

    canciones = playlist.canciones.all().order_by("-popularidad")

    return render(request, "catalogo/detalle_playlist.html", {"playlist": playlist, "canciones": canciones,})