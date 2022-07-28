from django.db import models
import uuid


class ShopUnit(models.Model):
    OFFER = 'OFFER'
    CATEGORY = 'CATEGORY'
    type_choices = [
        (OFFER, 'Offer'),
        (CATEGORY, 'Category'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, editable=False)
    name = models.CharField(null=False, max_length=255)
    date = models.CharField(null=False, max_length=255)
    type = models.CharField(max_length=8, choices=type_choices, null=False)
    parentId = models.UUIDField(primary_key=False, null=True, editable=False)
    price = models.IntegerField(null=True)
    children = models.TextField(null=True)

# Create your models here.
