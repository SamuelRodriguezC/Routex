from rest_framework import routers
from .api import StatusViewSet, PriorityViewSet,RouteViewSet, ExecutionLogsViewSet

# Creamos un router que generará las rutas automáticamente.
router = routers.DefaultRouter()

# Registramos el ViewSet.
# Esto crea las rutas para listar, crear, editar y eliminar tareas.
router.register('api/statuses', StatusViewSet, 'estatuses')
router.register('api/priorities', PriorityViewSet, 'priorities')
router.register('api/routes', RouteViewSet, 'routes')
router.register('api/executionlogs', ExecutionLogsViewSet, 'execution_logs')

# Guardamos todas las rutas generadas.
urlpatterns = router.urls 