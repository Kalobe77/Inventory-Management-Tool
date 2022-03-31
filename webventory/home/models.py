from django.db import models
from django.contrib.auth.models import AbstractUser, User
from typing import List
from datetime import date
# Create your models here.


class Item(models.Model):
    """Model for Items.

    Args:
        models ([type]): Inherits from Django Model's class.

    Returns:
        Item : object of an Item.
    """
    id: int = models.AutoField(unique=True, primary_key=True)
    name: str = models.CharField(max_length=30)
    description: str = models.CharField(max_length=100)
    quantity: int = models.IntegerField()
    price: float = models.DecimalField(max_digits=9, decimal_places=2)
    user_visibility: str = models.TextField()
    owner: User = models.ForeignKey(
        User, models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return " ".join([str(self.name).title(), f"({str(self.id)})"])

    def get_user_visibility(self) -> List[str]:
        return self.user_visibility.split(',')

    def owner(self) -> str:
        return self.owner.username


class User(AbstractUser):
    """Model for Users

    Args:
        AbstractUser ([type]): Inherits Django's AbstractUser Object.

    Returns:
        User: User for Webventory software.
    """
    username: str = models.CharField(max_length=30, unique=True)
    email: str = models.CharField(max_length=100)
    password: str = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.username


class ItemHistory(models.Model):
    """Model for ItemHistory

    Args:
        models ([type]): Inherits from Django model's class.

    Returns:
        ItemHistory: ItemHistory object.
    """

    item_id = models.ForeignKey(
        Item,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    quantity_before: int = models.IntegerField()
    quantity_after: int = models.IntegerField()
    price_before: float = models.FloatField()
    price_after: float = models.FloatField()
    date_of_change: date = models.DateTimeField()

    def __str__(self) -> str:
        return " ".join([str(self.item_id.name), "Change:", "on",
                         str(self.date_of_change)])


class Permissions(models.Model):
    id = models.ForeignKey(Item, models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
