from rest_framework import serializers
from airport.models import AirplaneType, Airplane, Airport, Route, Crew, Flight, Order, Ticket


class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ["id", "name", "closest_big_city"]


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ["id", "distance", "source", "destination"]


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["id", "name"]


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name")

    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats_in_row", "airplane_type"]


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name"]


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.CharField(read_only=True)
    airplane = serializers.CharField(read_only=True)

    class Meta:
        model = Flight
        fields = ["id", "departure_time", "arrival_time", "route", "airplane", "crew"]


class FlightListSerializer(FlightSerializer):
    crew = serializers.SlugRelatedField(many=True, read_only=True, slug_field="first_name")


class FlightDetailSerializer(FlightSerializer):
    crew = CrewSerializer(many=True, read_only=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "order", "flight"]


class TicketListSerializer(TicketSerializer):
    flight = serializers.CharField(read_only=True)


class TicketDetailSerializer(TicketSerializer):
    flight = FlightDetailSerializer(read_only=True)


class TicketSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat"]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "user", "tickets"]


class OrderListSerializer(OrderSerializer):
    tickets = TicketSummarySerializer(many=True, read_only=True)


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
