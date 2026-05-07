from django.contrib import admin

from airport.models import (
    Facility,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Crew
)


admin.site.register(Facility)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Crew, list_filter=("role", ))

