from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Item(models.Model):
    """Model for Items.

    Args:
        models ([type]): Inherits from Django Model's class.

    Returns:
        Item : object of an Item.
    """
    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=9,decimal_places=2)
    user_visibility = models.TextField()

    def __str__(self):
        return " ".join([str(self.name).title(), f"({str(self.id)})"])

    def get_user_visibility(self):
        return self.user_visibility.split(',')


class User(AbstractUser):
    """Model for Users

    Args:
        AbstractUser ([type]): Inherits Django's AbstractUser Object.

    Returns:
        User: User for Webventory software.
    """
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=30)

    def __str__(self):
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
    quantity_before = models.IntegerField()
    quantity_after = models.IntegerField()
    price_before = models.FloatField()
    price_after = models.FloatField()
    date_of_change = models.DateTimeField()

    def __str__(self):
        return " ".join([str(self.item_id.name), "Change:", "on",
                         str(self.date_of_change)])
