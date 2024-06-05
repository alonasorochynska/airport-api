from rest_framework import viewsets

from airport.models import (
    Airport, AirplaneType, Crew, Flight, Order, Ticket, Airplane, Route
)
from airport.serializers import (
    airport_serializer, airplane_serializers, crew_serializers,
    flight_serializers, order_serializers, route_serializers,
    ticket_serializers
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = airport_serializer.AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = route_serializers.RouteSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = airplane_serializers.AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = airplane_serializers.AirplaneSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = crew_serializers.CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = flight_serializers.FlightSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = order_serializers.OrderSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = ticket_serializers.TicketSerializer
