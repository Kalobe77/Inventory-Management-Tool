from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Item(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    user_visibility = models.CharField(max_length=30)

    def __str__(self):
        return str(str(self.name).title()) + ' (' + str(self.id) + ')'


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class ItemHistory(models.Model):
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
        return " ".join([str(self.item_id.name), "Change:", str(self.quantity_after), "on",
                         str(self.date_of_change.month) + "/" + str(self.date_of_change.day) + "/" + str(
                             self.date_of_change.year)])
