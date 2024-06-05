from rest_framework import serializers
from airport.models import Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["id", "departure_time", "arrival_time", "route", "airplane", "crew"]
