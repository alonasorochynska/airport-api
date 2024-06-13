import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if Airport.objects.filter(name=self.name).exists():
            raise ValidationError("This airport already exists.")
        super(Airport, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Route(models.Model):
    distance = models.IntegerField()
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="source_routes")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destination_routes")

    @property
    def get_names_of_airports(self) -> str:
        return f"{self.source} -> {self.destination}"

    def save(self, *args, **kwargs):
        if self.source == self.destination:
            raise ValidationError("Source and destination airports must be different")

        if Route.objects.filter(distance=self.distance, source=self.source, destination=self.destination).exists():
            raise ValidationError("Route with these details already exists.")

        super(Route, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.source}->{self.destination}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if AirplaneType.objects.filter(name=self.name).exists():
            raise ValidationError("This type of airplane already exists.")
        super(AirplaneType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def airplane_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/airplanes/", filename)


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name="airplanes")
    image = models.ImageField(null=True, upload_to=airplane_image_file_path)

    class Meta:
        unique_together = ("name", "rows", "seats_in_row", "airplane_type",)

    def __str__(self):
        return self.name

    @property
    def capacity(self):
        return self.rows * self.seats_in_row


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if Crew.objects.filter(first_name=self.first_name, last_name=self.last_name).exists():
            raise ValidationError("This crew member already exists.")
        super(Crew, self).save(*args, **kwargs)


class Flight(models.Model):
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")
    crew = models.ManyToManyField(Crew, related_name="flights")

    @staticmethod
    def format_time(dt):
        date_part = dt.strftime("%Y-%m-%d")
        time_part = dt.strftime("%H:%M")
        return f"{date_part}, {time_part}"

    def __str__(self):
        return f"{self.format_time(self.departure_time)} -> {self.format_time(self.arrival_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

    def __str__(self):
        return f"row: {self.row}, seat: {self.seat}"

    @property
    def get_place(self):
        return f"row: {self.row}, seat: {self.seat}"

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} number "
                                          f"must be in available range: "
                                          f"(1, {airplane_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row, self.seat, self.flight.airplane, ValidationError
        )

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )
