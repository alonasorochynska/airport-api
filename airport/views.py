from django.db.models import F, Count
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from airport.models import (
    Airport, AirplaneType, Crew, Flight, Order, Ticket, Airplane, Route
)
from airport.serializers import (
    AirportSerializer, RouteSerializer, AirplaneTypeSerializer, AirplaneSerializer,
    CrewSerializer, FlightSerializer, OrderSerializer, TicketSerializer,
    FlightListSerializer, FlightDetailSerializer, TicketListSerializer,
    TicketDetailSerializer, OrderListSerializer, AirplaneImageSerializer
)


class AirportViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer


class AirplaneTypeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action == "upload_image":
            return AirplaneImageSerializer
        return self.serializer_class

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=(IsAdminUser,),
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CrewViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = Flight.objects.select_related(
            "route__source", "route__destination", "airplane"
        ).prefetch_related("crew").annotate(
            tickets_available=(
                    F("airplane__rows") * F("airplane__seats_in_row") - Count("tickets")
            )
        )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return self.serializer_class


class TicketViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Ticket.objects.select_related("flight__route__source",
                                             "flight__route__destination")
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TicketDetailSerializer
        return self.serializer_class


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = (Order.objects.select_related("user")
                .prefetch_related("tickets__flight__route__source",
                                  "tickets__flight__route__destination"))
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
