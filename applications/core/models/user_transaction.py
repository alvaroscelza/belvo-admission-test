from django.db import models

from applications.core.managers.user_transactions_manager import UserTransactionsQuerySet
from applications.core.models.category import Category


class UserTransaction(models.Model):
    class TransactionType(models.TextChoices):
        INFLOW = 'inflow', 'inflow'
        OUTFLOW = 'outflow', 'outflow'

    objects = UserTransactionsQuerySet.as_manager()

    reference = models.CharField(max_length=6, unique=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(choices=TransactionType.choices, max_length=7, default=TransactionType.INFLOW)
    category = models.ForeignKey(Category, models.CASCADE)
    user_email = models.EmailField(max_length=100)
