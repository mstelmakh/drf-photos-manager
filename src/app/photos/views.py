from rest_framework import viewsets

from photos.models import Photo
from photos.serializers import PhotoSerializer


class PhotoView(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
