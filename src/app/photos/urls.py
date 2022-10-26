from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

from .views import FetchPhotos


router = DefaultRouter()

router.register('photos', views.PhotoView)


urlpatterns = [
    path('', include(router.urls)),
    path('photos/fetch/all/', FetchPhotos.as_view()),
    path('photos/fetch/<int:n>/', FetchPhotos.as_view()),
]
