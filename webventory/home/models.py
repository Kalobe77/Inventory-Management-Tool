from django.db import models


# Create your models here.
class Item(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    user_visability = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name) + ' (' + str(self.id) + ')'


class User(models.Model):
    user_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.user_name


class ItemHistory(models.Model):
    item_id = models.ForeignKey(
        Item,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    change = models.IntegerField()
    date_of_change = models.DateField()

    def __str__(self):
        return " ".join([str(self.item_id.name), "Change:", str(self.change), "on", str(self.date_of_change.month) + "/" + str(self.date_of_change.day) + "/" + str(self.date_of_change.year)])

