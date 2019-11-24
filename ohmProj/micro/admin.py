

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    list_per_page = 15
    search_fields = ['username']

    fieldsets = [
        (None, {'fields': ['username', 'password', 'first_name', 'last_name', 'email', 'telephone']}),
        ("User Management", {
            'fields': ['last_login', 'date_joined'], 'classes': ['collapse']}),
        ("User Permissions", {
            'fields': ['groups', 'user_permissions', 'is_active'], 'classes': ['collapse']})
    ]


admin.site.register(User, UserAdmin)