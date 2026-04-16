# routes/views/routes_execution_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from logistics.models import Route, Status
from logistics.serializers.routes_execution_serializer import RoutesExecutionSerializer
from logistics.services.routes_execution_service import RoutesExecutionService


class RoutesExecutionView(APIView):

    def post(self, request):

        serializer = RoutesExecutionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        route_ids = serializer.validated_data["route_ids"]

        routes = Route.objects.select_related("status").filter(id__in=route_ids)

        # -----------------------------
        # Mapeo de estados (cache simple)
        # -----------------------------
        statuses = {
            s.description.upper(): s
            for s in Status.objects.all()
        }

        service = RoutesExecutionService(status_map=statuses)

        result = service.execute(routes)

        return Response(result, status=status.HTTP_200_OK)