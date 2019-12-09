from django.urls import path, include
from rest_framework.routers import DefaultRouter

from personal_okr import views
router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'personal_okr'
urlpatterns = [
    path('', include(router.urls))
]