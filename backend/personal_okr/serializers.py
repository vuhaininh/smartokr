from rest_framework import serializers
from personal_okr.models import Tag, Objective


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ObjectiveSerializer(serializers.ModelSerializer):
    """Serializer for objective objects"""
    class Meta:
        model = Objective
        fields = ('id', 'user', 'description', 'finished_date')
        read_only_fields = ('id',)
