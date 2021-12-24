from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.core.serializers.user_transactions_serializers import UserTransactionsSerializer


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
