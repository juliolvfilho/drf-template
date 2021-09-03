import hashlib
from rest_framework.throttling import SimpleRateThrottle


class DebounceThrottle(SimpleRateThrottle):
    """
    Prevents a user from making the same API call twice in a very short period.
    """

    def get_rate(self):
        return self.THROTTLE_RATES.get("debounce", "1/sec")

    def get_scope(self, request):
        """
        Unique scope by http request
        """
        return request.method + "." + request.GET.urlencode(safe="()")

    def get_ident(self, request):
        """
        The user id will be used as a unique cache key if the user is
        authenticated. For anonymous requests, a combination of IP address and
        UserAgent hash will be used.
        """
        if request.user:
            return request.user["uid"]
        else:
            return (
                super().get_ident(request)
                + "."
                + hashlib.md5(
                    request.META.get("HTTP_USER_AGENT", "").encode()
                ).hexdigest()
            )

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.get_scope(request),
            "ident": self.get_ident(request),
        }
