from rest_framework import views
from rest_framework.response import Response

from imports.services import import_photos_from_api, import_photos_from_json


class ImportPhotosFromApi(views.APIView):
    """
    View used to import photos from external api.
    Only GET method supported.

    For slicing pass the start (default: 0) and limit arguments.
    """
    def get(self, request, *args, **kwargs):
        start = int(request.GET.get('start', 0))
        limit = request.GET.get('limit')
        limit = int(limit) if limit else None
        photos = import_photos_from_api(start, limit)
        return Response(photos)


class ImportPhotosFromJson(views.APIView):
    """
    View used to import photos from JSON file.
    Only GET method supported.

    For slicing pass the start (default: 0) and limit arguments.
    """
    def get(self, request, *args, **kwargs):
        start = int(request.GET.get('start', 0))
        limit = request.GET.get('limit')
        limit = int(limit) if limit else None
        photos = import_photos_from_json(start=start, limit=limit)
        return Response(photos)
