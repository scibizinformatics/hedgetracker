from rest_framework import viewsets

from main.serializers import MetricSerializer
from main.models import Metric


class MetricViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricSerializer
    queryset = Metric.objects.all()
