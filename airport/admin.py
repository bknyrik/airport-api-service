from django.contrib import admin
from django.contrib.admin.options import TabularInline

from airport.models import (
    Facility,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Crew,
    Flight,
    Ticket,
    Order
)


class TicketInline(TabularInline):
    model = Ticket
    extra = 1


class FlightInline(TabularInline):
    model = Flight
    extra = 1


admin.site.register(Facility)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Route, inlines=(FlightInline, ))
admin.site.register(Crew, list_filter=("role", ))
admin.site.register(Flight)
admin.site.register(Order, inlines=(TicketInline, ))
admin.site.register(Ticket, list_display=("order", "flight", "row", "seat"))
