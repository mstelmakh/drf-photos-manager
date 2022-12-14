from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views


router = DefaultRouter()

router.register('photos', views.PhotoView)


urlpatterns = [
    path('', include(router.urls)),
    path('photos/import/', include('imports.urls')),
]
