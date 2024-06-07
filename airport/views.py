from rest_framework import viewsets

from airport.models import (
    Airport, AirplaneType, Crew, Flight, Order, Ticket, Airplane, Route
)
from airport.serializers import (
    AirportSerializer, RouteSerializer, AirplaneTypeSerializer, AirplaneSerializer,
    CrewSerializer, FlightSerializer, OrderSerializer, TicketSerializer,
    FlightListSerializer, FlightDetailSerializer, OrderListSerializer, OrderDetailSerializer, TicketListSerializer,
    TicketDetailSerializer
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = Flight.objects.select_related(
            "route__source", "route__destination", "airplane"
        ).prefetch_related("crew")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return self.serializer_class


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("flight__route__source",
                                             "flight__route__destination")
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TicketDetailSerializer
        return self.serializer_class


class OrderViewSet(viewsets.ModelViewSet):
    queryset = (Order.objects.select_related("user")
                .prefetch_related("tickets__flight__route__source",
                                  "tickets__flight__route__destination"))
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderDetailSerializer
        return self.serializer_class



