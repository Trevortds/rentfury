from django.db import models
from carts.models import Cart

# Create your models here.
class Order(models.Model):
    billing_profile = models.CharField(max_length=120)
    shipping_address = None
    billing_address = None
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    status = models.CharField(max_length=120, default='created')