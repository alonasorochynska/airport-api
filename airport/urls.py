from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirportViewSet, RouteViewSet, AirplaneTypeViewSet, AirplaneViewSet,
    CrewViewSet, FlightViewSet, OrderViewSet, TicketViewSet,
)

router = routers.DefaultRouter()
router.register("airport", AirportViewSet)
router.register("route", RouteViewSet)
router.register("airplane-type", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("crew", CrewViewSet)
router.register("flight", FlightViewSet)
router.register("order", OrderViewSet)
router.register("ticket", TicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
