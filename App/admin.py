from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'web_terms', 'dataprocessing', 'subscription', 'created_date', 'modified_date']
    search_fields = ['username']

admin.site.register(CustomUser, CustomUserAdmin)
















    











