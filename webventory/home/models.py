from django.db import models

# Create your models here.
class Item(models.Model):
    id = models.IntegerField.unique()
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    user_visability = models.CharField(max_length=30)


class User(models.Model):
    user_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=30)

class ItemHistory(models.Model):
    change = models.IntegerField()
    date_of_change = models.DateField()
    id = models.ForeignKey(
        Item,
        models.SET_NULL,
        blank=True,
        null=True,
    )