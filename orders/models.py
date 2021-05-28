from django.db import models
from products.models import Product
from users.models import User
from .validators import validate_number
from django.utils.timezone import datetime


class Order(models.Model):
    product = models.ForeignKey(
        Product, related_name="orders", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User, related_name="orders", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    full_name = models.CharField(max_length=180)
    address = models.CharField(max_length=180)
    phone_number = models.CharField(
        max_length=10, validators=[validate_number])
    email = models.EmailField(max_length=254, blank=True)
    completed = models.BooleanField(default=False)
    date_ordered = models.DateField(default=datetime.now)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return f"Order {self.id}"
