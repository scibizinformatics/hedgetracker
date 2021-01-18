from rest_framework import viewsets
from rest_framework.response import Response

from main.serializers import MetricSerializer, MetricListSerializer
from main.models import Metric


class MetricViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricSerializer
    queryset = Metric.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = MetricListSerializer(queryset)
        return Response(serializer.data)
