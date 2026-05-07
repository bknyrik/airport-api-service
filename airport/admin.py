from django.contrib import admin

from airport.models import (
    Facility,
    AirplaneType,
    Airplane,
    Airport,
    Route,
)


admin.site.register(Facility)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Route)
