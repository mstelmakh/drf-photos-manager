from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

from .views import ImportPhotosFromApi, ImportPhotosFromJson


router = DefaultRouter()

router.register('photos', views.PhotoView)


urlpatterns = [
    path('', include(router.urls)),
    path('photos/import/api/all/', ImportPhotosFromApi.as_view()),
    path('photos/import/api/<int:n>/', ImportPhotosFromApi.as_view()),
    path('photos/import/json/all/', ImportPhotosFromJson.as_view()),
    path('photos/import/json/<int:n>/', ImportPhotosFromJson.as_view()),
]
