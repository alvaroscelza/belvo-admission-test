from django.db import models


class UserTransactionsQuerySet(models.QuerySet):
    def create(self, **kwargs):
        super().create(**kwargs)
