from rest_framework import serializers

from .models import Assignment, Event, Photographer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    photographer = PhotographerSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = '__all__'
