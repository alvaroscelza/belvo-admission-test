from django.db import models

from applications.core.managers.user_transactions_manager import UserTransactionsQuerySet


class UserTransaction(models.Model):
    class TransactionTypes(models.TextChoices):
        INFLOW = 'inflow', 'inflow'
        OUTFLOW = 'outflow', 'outflow'

    objects = UserTransactionsQuerySet.as_manager()

    reference = models.CharField(max_length=6, unique=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(choices=TransactionTypes.choices, max_length=7, default=TransactionTypes.INFLOW)
    category = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100)
