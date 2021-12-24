from rest_framework import viewsets

from applications.core.serializers.user_transactions_serializers import UserTransactionsSerializer


class UserTransactionsView(viewsets.ModelViewSet):
    serializer_class = UserTransactionsSerializer
    queryset = serializer_class.Meta.model.objects.all()
