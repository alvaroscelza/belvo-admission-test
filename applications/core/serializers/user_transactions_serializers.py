from rest_framework import serializers

from applications.core.models import UserTransaction


class UserTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransaction
        fields = '__all__'
