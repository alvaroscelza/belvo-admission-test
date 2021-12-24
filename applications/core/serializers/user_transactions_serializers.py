from rest_framework import serializers

from applications.core.models import UserTransaction


class UserTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransaction
        fields = '__all__'


class UserTransactionsGroupedByTypesSerializer(serializers.Serializer):
    user_email = serializers.CharField()
    total_inflow = serializers.CharField()
    total_outflow = serializers.CharField()

    def update(self, instance, validated_data):
        raise NotImplementedError('this serializer is not supposed to create nor update anything')

    def create(self, validated_data):
        raise NotImplementedError('this serializer is not supposed to create nor update anything')
