import os
import django
from rest_framework.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airport_core.settings")
django.setup()

from django.test import TestCase
from airport.models import Airport, Route, AirplaneType, Airplane, Crew, Flight, Order, Ticket
from airport.serializers import (
    AirportSerializer, RouteSerializer, AirplaneTypeSerializer,
    AirplaneSerializer, CrewSerializer, FlightSerializer,
    OrderSerializer, TicketSerializer
)
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta


class AirportModelTest(TestCase):
    def setUp(self):
        self.airport = Airport.objects.create(name="Test Airport", closest_big_city="Test City")

    def test_create_airport(self):
        self.assertEqual(self.airport.name, "Test Airport")
        self.assertEqual(self.airport.closest_big_city, "Test City")

    def test_duplicate_airport(self):
        with self.assertRaises(ValidationError) as context:
            Airport.objects.create(name="Test Airport", closest_big_city="Another City")
        self.assertEqual(str(context.exception.detail[0]), "This airport already exists.")


class RouteModelTest(TestCase):
    def setUp(self):
        self.airport1 = Airport.objects.create(name="Airport 1", closest_big_city="City 1")
        self.airport2 = Airport.objects.create(name="Airport 2", closest_big_city="City 2")
        self.route = Route.objects.create(distance=100, source=self.airport1, destination=self.airport2)

    def test_create_route(self):
        self.assertEqual(self.route.distance, 100)
        self.assertEqual(self.route.source, self.airport1)
        self.assertEqual(self.route.destination, self.airport2)

    def test_duplicate_route(self):
        with self.assertRaises(ValidationError):
            Route.objects.create(distance=100, source=self.airport1, destination=self.airport2)

    def test_same_source_destination(self):
        with self.assertRaises(ValidationError):
            Route.objects.create(distance=100, source=self.airport1, destination=self.airport1)


class AirplaneTypeModelTest(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Test Airplane Type")

    def test_create_airplane_type(self):
        self.assertEqual(self.airplane_type.name, "Test Airplane Type")

    def test_duplicate_airplane_type(self):
        with self.assertRaises(ValidationError):
            AirplaneType.objects.create(name="Test Airplane Type")


class AirplaneModelTest(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Test Airplane Type")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type
        )

    def test_create_airplane(self):
        self.assertEqual(self.airplane.name, "Test Airplane")
        self.assertEqual(self.airplane.rows, 10)
        self.assertEqual(self.airplane.seats_in_row, 6)
        self.assertEqual(self.airplane.airplane_type, self.airplane_type)

    def test_airplane_capacity(self):
        self.assertEqual(self.airplane.capacity, 60)


class CrewModelTest(TestCase):
    def setUp(self):
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")

    def test_create_crew(self):
        self.assertEqual(self.crew.first_name, "John")
        self.assertEqual(self.crew.last_name, "Doe")
        self.assertEqual(self.crew.full_name, "John Doe")

    def test_duplicate_crew(self):
        with self.assertRaises(ValidationError):
            Crew.objects.create(first_name="John", last_name="Doe")


class FlightModelTest(TestCase):
    def setUp(self):
        self.airport1 = Airport.objects.create(name="Airport 1", closest_big_city="City 1")
        self.airport2 = Airport.objects.create(name="Airport 2", closest_big_city="City 2")
        self.route = Route.objects.create(distance=100, source=self.airport1, destination=self.airport2)
        self.airplane_type = AirplaneType.objects.create(name="Test Airplane Type")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type
        )
        self.flight = Flight.objects.create(
            departure_time=datetime.now(),
            arrival_time=datetime.now() + timedelta(hours=2),
            route=self.route,
            airplane=self.airplane
        )

    def test_create_flight(self):
        self.assertEqual(self.flight.route, self.route)
        self.assertEqual(self.flight.airplane, self.airplane)


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="testuser@example.com", password="testpass123")
        self.order = Order.objects.create(user=self.user)

    def test_create_order(self):
        self.assertEqual(self.order.user, self.user)

class AirportSerializerTest(TestCase):
    def test_airport_serializer(self):
        airport = Airport.objects.create(name="Test Airport", closest_big_city="Test City")
        serializer = AirportSerializer(airport)
        self.assertEqual(serializer.data["name"], "Test Airport")
        self.assertEqual(serializer.data["closest_big_city"], "Test City")


class RouteSerializerTest(TestCase):
    def test_route_serializer(self):
        airport1 = Airport.objects.create(name="Airport 1", closest_big_city="City 1")
        airport2 = Airport.objects.create(name="Airport 2", closest_big_city="City 2")
        route = Route.objects.create(distance=100, source=airport1, destination=airport2)
        serializer = RouteSerializer(route)
        self.assertEqual(serializer.data["distance"], 100)
        self.assertEqual(serializer.data["source"], "City 1")
        self.assertEqual(serializer.data["destination"], "City 2")


class AirplaneTypeSerializerTest(TestCase):
    def test_airplane_type_serializer(self):
        airplane_type = AirplaneType.objects.create(name="Test Airplane Type")
        serializer = AirplaneTypeSerializer(airplane_type)
        self.assertEqual(serializer.data["name"], "Test Airplane Type")


class AirplaneSerializerTest(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Test Airplane Type")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type
        )

    def test_airplane_serializer(self):
        serializer = AirplaneSerializer(self.airplane)
        self.assertEqual(serializer.data["name"], "Test Airplane")
        self.assertEqual(serializer.data["rows"], 10)
        self.assertEqual(serializer.data["seats_in_row"], 6)
        self.assertEqual(serializer.data["airplane_type"], "Test Airplane Type")


class CrewSerializerTest(TestCase):
    def test_crew_serializer(self):
        crew = Crew.objects.create(first_name="John", last_name="Doe")
        serializer = CrewSerializer(crew)
        self.assertEqual(serializer.data["first_name"], "John")
        self.assertEqual(serializer.data["last_name"], "Doe")


class FlightSerializerTest(TestCase):
    def setUp(self):
        self.airport1 = Airport.objects.create(name="Airport 1", closest_big_city="City 1")
        self.airport2 = Airport.objects.create(name="Airport 2", closest_big_city="City 2")
        self.route = Route.objects.create(distance=100, source=self.airport1, destination=self.airport2)
        self.airplane_type = AirplaneType.objects.create(name="Test Airplane Type")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type
        )
        self.flight = Flight.objects.create(
            departure_time=datetime.now(),
            arrival_time=datetime.now() + timedelta(hours=2),
            route=self.route,
            airplane=self.airplane
        )

    def test_flight_serializer(self):
        serializer = FlightSerializer(self.flight)
        self.assertEqual(serializer.data["route"], "Airport 1 -> Airport 2")
        self.assertEqual(serializer.data["airplane"], "Test Airplane")


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="testuser@example.com", password="testpass123")
        self.order = Order.objects.create(user=self.user)

    def test_order_serializer(self):
        serializer = OrderSerializer(self.order)
        print(serializer.data)
        self.assertEqual(serializer.data["id"], self.user.id)


class TicketSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="testuser@example.com", password="testpass123")
        self.airport1 = Airport.objects.create(name="Airport 1", closest_big_city="City 1")
        self.airport2 = Airport.objects.create(name="Airport 2", closest_big_city="City 2")
        self.route = Route.objects.create(distance=100, source=self.airport1, destination=self.airport2)
        self.airplane_type = AirplaneType.objects.create(name="Test Airplane Type")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type
        )
        self.flight = Flight.objects.create(
            departure_time=datetime.now(),
            arrival_time=datetime.now() + timedelta(hours=2),
            route=self.route,
            airplane=self.airplane
        )
        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(row=1, seat=1, flight=self.flight, order=self.order)

    def test_ticket_serializer(self):
        serializer = TicketSerializer(self.ticket)
        self.assertEqual(serializer.data["row"], 1)
        self.assertEqual(serializer.data["seat"], 1)
        self.assertEqual(serializer.data["flight"], self.flight.id)
        self.assertEqual(serializer.data["order"], self.order.id)
