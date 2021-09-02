from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response


class ItWorksAPIView(APIView):
    def get(self, request):
        response = {"it_works": True}
        if settings.DEBUG:
            response["user"] = request.user
        return Response(response)

    def post(self, request):
        response = {"it_works": True}
        if settings.DEBUG:
            response["user"] = request.user
            response["received"] = request.data
        return Response(response)
