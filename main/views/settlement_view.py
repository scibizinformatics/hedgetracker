from rest_framework import viewsets

from main.serializers import SettlementSerializer
from main.models import Settlement


class SettlementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SettlementSerializer
    queryset = Settlement.objects.all()
