from django.urls import path, include
from rest_framework.routers import DefaultRouter

from personal_okr import views
router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('objectives', views.ObjectiveViewSet)
router.register('keyresults', views.KeyResultViewSet)
app_name = 'personal_okr'
urlpatterns = [
    path('', include(router.urls))
]
