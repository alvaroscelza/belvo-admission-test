from django.db import models
from rest_framework.exceptions import ValidationError


class UserTransactionsQuerySet(models.QuerySet):
    def create(self, **kwargs):
        self.check_transaction_type(**kwargs)
        return super().create(**kwargs)

    @staticmethod
    def check_transaction_type(**kwargs):
        transaction_type = kwargs['type']
        amount = kwargs['amount']
        if transaction_type == 'inflow' and amount <= 0:
            raise ValidationError('All inflow transactions amounts are positive decimal numbers.')
        if transaction_type == 'outflow' and amount >= 0:
            raise ValidationError('All outflow transactions amounts are negative decimal numbers.')
