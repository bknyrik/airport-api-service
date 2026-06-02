from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet
from django_filters import filters


class UserFilterSet(FilterSet):
    class Meta:
        model = get_user_model()
        fields = ("email", "is_staff")

    email = filters.CharFilter(
        field_name="email",
        lookup_expr="icontains"
    )
