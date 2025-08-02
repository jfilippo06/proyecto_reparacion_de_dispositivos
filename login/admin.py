# login/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_verified', 'is_staff')
    list_filter = ('user_type', 'is_verified', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('email', 'user_type')}),
        ('Permisos', {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(UserProfile, UserProfileAdmin)