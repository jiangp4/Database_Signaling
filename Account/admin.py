from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):    
    ordering = ('username',)
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'institute', 'url', 'bio']
    search_fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'institute', 'bio')

admin.site.register(Account, AccountAdmin)
