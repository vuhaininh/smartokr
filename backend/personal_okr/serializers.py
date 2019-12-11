from rest_framework import serializers
from personal_okr.models import Tag, Objective, KeyResult


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ObjectiveSerializer(serializers.ModelSerializer):
    """Serializer for objective objects"""
    key_results = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Objective
        fields = ('id', 'description', 'finished_date', 'key_results')
        read_only_fields = ('id',)


class KeyResultSerializer(serializers.ModelSerializer):
    """Serializer for key result objects"""

    class Meta:
        model = KeyResult
        fields = ('id', 'description', 'finished_date', 'objective')
        read_only_fields = ('id',)
