from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response

from photos.models import Photo
from photos.serializers import PhotoSerializer

from fetching.services import import_photos_from_api, import_photos_from_json


class PhotoView(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class ImportPhotosFromApi(views.APIView):
    """
    View used to import photos from external api.
    Only GET method supported.
    Takes one argument - number of photos to import,
    if no argument is provided, imports all available photos.
    """
    def get(self, request, n=None, *args, **kwargs):
        if n:
            photos = import_photos_from_api(n=n)
        else:
            photos = import_photos_from_api()
        return Response(photos)


class ImportPhotosFromJson(views.APIView):
    """
    View used to import photos from JSON file.
    Only GET method supported.
    Takes one argument - number of photos to import,
    if no argument is provided, imports all available photos.
    """
    def get(self, request, n=None, *args, **kwargs):
        if n:
            photos = import_photos_from_json(n=n)
        else:
            photos = import_photos_from_json()
        return Response(photos)
