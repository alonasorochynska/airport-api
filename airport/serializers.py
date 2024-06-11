from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import AirplaneType, Airplane, Airport, Route, Crew, Flight, Order, Ticket


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["id", "name", "closest_big_city"]


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all())
    destination = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all())

    class Meta:
        model = Route
        fields = ["id", "distance", "source", "destination"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["source"] = instance.source.closest_big_city
        representation["destination"] = instance.destination.closest_big_city
        return representation


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["id", "name"]


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.PrimaryKeyRelatedField(queryset=AirplaneType.objects.all())

    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats_in_row", "capacity", "airplane_type"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["airplane_type"] = instance.airplane_type.name
        return representation


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name"]


class TicketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "get_place"]


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.select_related("source", "destination")
    )
    airplane = serializers.PrimaryKeyRelatedField(queryset=Airplane.objects.all())
    crew = serializers.PrimaryKeyRelatedField(queryset=Crew.objects.all(), many=True)
    departure_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    arrival_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Flight
        fields = ["id", "departure_time", "arrival_time", "route", "airplane", "crew"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["route"] = instance.route.get_names_of_airports
        representation["airplane"] = instance.airplane.name
        return representation


class FlightListSerializer(FlightSerializer):
    crew = serializers.SlugRelatedField(many=True, read_only=True, slug_field="full_name")


class FlightDetailSerializer(FlightSerializer):
    crew = CrewSerializer(many=True, read_only=True)
    taken_places = TicketPlaceSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Flight
        fields = FlightSerializer.Meta.fields + ["taken_places",]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "order", "flight"]

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError,
        )
        return data


class TicketListSerializer(TicketSerializer):
    flight = serializers.CharField(read_only=True)


class TicketDetailSerializer(TicketSerializer):
    flight = FlightDetailSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Order
        fields = ["id", "created_at", "tickets"]

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketPlaceSerializer(many=True, read_only=True)
