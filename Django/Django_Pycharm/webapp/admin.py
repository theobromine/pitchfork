from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import User
from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)


# admin.site.unregister(User)  # First unregistered the old class
# admin.site.register(Profile)
