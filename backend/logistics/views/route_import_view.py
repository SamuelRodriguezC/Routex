from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.route_import_service import RouteImportService


class RouteImportView(APIView):

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "No se envió ningún archivo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service = RouteImportService(file)
        result = service.process()

        return Response(result, status=status.HTTP_200_OK)