from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import User, Profile
from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)


# admin.site.unregister(User)  # First unregistered the old class
# admin.site.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']


admin.site.register(Profile, ProfileAdmin)
