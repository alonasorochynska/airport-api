from rest_framework import serializers
from airport.models import Route


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ["id", "distance", "source", "destination"]
