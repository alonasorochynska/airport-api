from django.contrib import admin
from django.db.models import Count

from airport.models import Airport, Route, AirplaneType, Airplane, Crew, Flight, Order, Ticket


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "closest_big_city")
    list_select_related = True
    ordering = ("name",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("id", "get_source_name", "get_destination_name", "distance")
    list_select_related = True
    ordering = ("id",)

    def get_source_name(self, obj):
        return obj.source.name

    def get_destination_name(self, obj):
        return obj.destination.name

    get_source_name.short_description = "Source"
    get_destination_name.short_description = "Destination"


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "count_airplanes")
    ordering = ("name",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(num_airplanes=Count('airplanes'))
        return queryset

    def count_airplanes(self, obj):
        return obj.num_airplanes

    count_airplanes.short_description = "Number of Airplanes"


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("name", "rows", "seats_in_row", "airplane_type")
    ordering = ("name",)


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("full_name",)
    ordering = ("first_name",)

    @staticmethod
    def full_name(obj):
        return f"{obj.first_name} {obj.last_name}"


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("route", "departure_time", "arrival_time")
    ordering = ("departure_time",)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)
    list_display = ("id", "created_at", "user")
    ordering = ("id",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("get_order_id", "flight", "place")
    ordering = ("id",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("flight", "order")
        return queryset

    @staticmethod
    def place(obj):
        return f"row: {obj.row}, seat: {obj.seat}"

    def get_order_id(self, obj):
        return obj.order.id

    get_order_id.short_description = "Order ID"
