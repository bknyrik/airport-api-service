from rest_framework.viewsets import ModelViewSet

from airport.models import Facility
from airport.serializers import FacilitySerializer


class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
