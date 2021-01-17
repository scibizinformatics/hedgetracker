from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from main.serializers import SettlementSerializer
from main.models import Settlement


class SettlementPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SettlementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SettlementSerializer
    queryset = Settlement.objects.all()
    pagination_class = SettlementPagination
