import django_filters
from logistics.models import Route


class RouteFilter(django_filters.FilterSet):

    #  filtros por relaciones (FK)
    priority = django_filters.NumberFilter(field_name="priority__id")
    status = django_filters.NumberFilter(field_name="status__id")

    #  filtros por fechas (rango)
    start_date = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte"
    )

    end_date = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte"
    )

    #  filtro opcional por ventana de tiempo de la ruta
    window_start = django_filters.DateTimeFilter(
        field_name="time_window_start",
        lookup_expr="gte"
    )

    window_end = django_filters.DateTimeFilter(
        field_name="time_window_end",
        lookup_expr="lte"
    )

    class Meta:
        model = Route
        fields = ["priority", "status"]