from rest_framework import serializers
from personal_okr.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""
    class Meta:
        model = Tag
        field = ('id', 'name')
        read_only_fields = ('id',)
