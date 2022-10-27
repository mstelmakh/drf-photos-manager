from .views import ImportPhotosFromApi, ImportPhotosFromJson

from django.urls import path


urlpatterns = [
    path('from-api', ImportPhotosFromApi.as_view()),
    path('from-json', ImportPhotosFromJson.as_view()),
]
