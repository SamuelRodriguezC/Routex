from rest_framework import routers
from logistics.views.routes_execution_view import RoutesExecutionView
from django.urls import path


from logistics.views import (
    RouteViewSet,
    StatusViewSet,
    PriorityViewSet,
    ExecutionLogsViewSet,
    RoutesExecutionView
)


# Creamos un router que generará las rutas automáticamente.
router = routers.DefaultRouter()

# Registramos el ViewSet.
router.register('api/statuses', StatusViewSet, 'estatuses')
router.register('api/priorities', PriorityViewSet, 'priorities')
router.register('api/routes', RouteViewSet, 'routes')
router.register('api/executionlogs', ExecutionLogsViewSet, 'execution_logs') # CRUD testear

urlpatterns = [
    path('api/routes/execute/', RoutesExecutionView.as_view(), name='routes-execute'),
]




# Guardamos todas las rutas generadas.
urlpatterns = router.urls 