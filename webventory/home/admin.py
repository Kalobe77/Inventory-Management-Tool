from django.contrib import admin

# Register your models here.
from home.models import User,Item,ItemHistory

admin.site.register(Item)
admin.site.register(User)
admin.site.register(ItemHistory)