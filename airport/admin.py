from django.contrib import admin

from airport.models import (
    Facility,
    AirplaneType,
    Airplane,
    Airport
)


admin.site.register(Facility)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airport)
