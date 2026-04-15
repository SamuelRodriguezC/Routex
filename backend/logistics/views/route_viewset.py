
from rest_framework import viewsets, permissions
from ..models import Route
from ..serializers import RouteSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from ..services.route_import_service import RouteImportService


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"], url_path="import")
    def import_routes(self, request):

        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "Debe enviar un archivo Excel"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = RouteImportService.import_routes(file)

        return Response(result, status=status.HTTP_200_OK)