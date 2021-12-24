from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.core.serializers.user_transactions_serializers import UserTransactionsSerializer


class UserTransactionsView(viewsets.ModelViewSet):
    serializer_class = UserTransactionsSerializer
    queryset = serializer_class.Meta.model.objects.all()

    @action(detail=False, methods=['post'])
    def create_bulk(self, request, *args, **kwargs):
        transactions_data = request.data.copy()
        for transaction_data in transactions_data:
            request.data = transaction_data
            self.create(request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED)
