from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response


class ItWorksAPIView(APIView):
    def get(self, request):
        return Response({"it_works": True})

    def post(self, request):
        return Response(
            {
                "received": request.data
                if settings.ENVIRONMENT == "development"
                else True
            }
        )
