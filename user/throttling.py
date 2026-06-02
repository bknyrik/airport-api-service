from typing import TYPE_CHECKING

from rest_framework.throttling import SimpleRateThrottle
from rest_framework.request import Request


if TYPE_CHECKING:
    from rest_framework.views import APIView


class AdminRateThrottle(SimpleRateThrottle):
    scope = "admin"

    def get_cache_key(self, request: Request, view: "APIView") -> str | None:
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return self.cache_format % {
                "scope": self.scope,
                "ident": request.user.pk
            }

        return None
