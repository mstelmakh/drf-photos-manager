from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

from .views import ImportPhotosFromApi, ImportPhotosFromJson


router = DefaultRouter()

router.register('photos', views.PhotoView)


urlpatterns = [
    path('', include(router.urls)),
    path('photos/import-from-api', ImportPhotosFromApi.as_view()),
    path('photos/import-from-json', ImportPhotosFromJson.as_view()),
]
