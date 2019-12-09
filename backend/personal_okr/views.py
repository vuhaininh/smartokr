from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from personal_okr.models import Tag, Objective
from personal_okr import serializers


class BasePersonalOkrAttrViewSet(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.CreateModelMixin):
    """Base viewset for user owned personal okr attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BasePersonalOkrAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the curretn authenticated users only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class ObjectiveViewSet(BasePersonalOkrAttrViewSet):
    """Manage objectives in the database"""
    queryset = Objective.objects.all()
    serializer_class = serializers.ObjectiveSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user"""
        return self.queryset.filter(user=self.request.user)\
            .order_by('-description')
