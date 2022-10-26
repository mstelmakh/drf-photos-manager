from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response

from photos.models import Photo
from photos.serializers import PhotoSerializer

from fetching.services import fetch_photos_to_database


class PhotoView(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class FetchPhotos(views.APIView):

    def get(self, request, n=None, *args, **kwargs):
        if n:
            photos = fetch_photos_to_database(n)
        else:
            photos = fetch_photos_to_database()
        return Response(photos)
