from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import User, Item

# admin.site.unregister(User)  # First unregistered the old class
admin.site.register(Item)
