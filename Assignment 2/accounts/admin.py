from django.contrib import admin

from .models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'gender',
    )
    ordering = ['id']

admin.site.register(Profile, ProfileAdmin)
