from django.db.models import DecimalField, Q, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.core.serializers.user_transactions_serializers import (UserTransactionsGroupedByTypesSerializer,
                                                                         UserTransactionsSerializer)


class UserTransactionsView(viewsets.ModelViewSet):
    serializer_class = UserTransactionsSerializer
    queryset = serializer_class.Meta.model.objects.all()

    @action(detail=False, methods=['post'])
    def create_bulk(self, request, *args, **kwargs):
        serializer = UserTransactionsSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def types_per_user(self, request, *args, **kwargs):
        total_inflow = Coalesce(Sum('amount', filter=Q(type='inflow')), Value(0.0), output_field=DecimalField())
        total_outflow = Coalesce(Sum('amount', filter=Q(type='outflow')), Value(0.0), output_field=DecimalField())
        query_grouped_by_user = self.queryset.values('user_email')
        query = query_grouped_by_user.annotate(total_inflow=total_inflow).annotate(total_outflow=total_outflow)
        serializer = UserTransactionsGroupedByTypesSerializer(query, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_summary(self, request, *args, **kwargs):
        try:
            user_email = request.query_params['user_email']
            query = self.queryset.filter(user_email=user_email).values('type', 'category').annotate(Sum('amount'))
            inflow_results = query.filter(type='inflow')
            outflow_results = query.filter(type='outflow')

            inflow = {}
            for result in inflow_results:
                inflow[result['category']] = result['amount__sum']

            outflow = {}
            for result in outflow_results:
                outflow[result['category']] = result['amount__sum']

            data = {'inflow': inflow, 'outflow': outflow}
            return Response(data)
        except KeyError:
            return Response('user_email is required.', status=status.HTTP_400_BAD_REQUEST)
