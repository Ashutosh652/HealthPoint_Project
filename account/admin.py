from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserAdminConfig(UserAdmin):
	search_fields = ('user_name', 'email', 'full_name')
	list_filter = ('user_name', 'full_name', 'email', 'is_active', 'is_staff', 'is_doctor')
	ordering = ('date_joined',)
	list_display = ('email', 'user_name', 'full_name', 'is_active', 'is_staff', 'is_doctor')
	fieldsets = (
		(None, {'fields': ('email', 'user_name', 'full_name',)}),
		('Permissions', {'fields': ('is_staff', 'is_active', 'is_doctor', 'is_superuser')}),
		)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'user_name', 'full_name', 'password1', 'password2', 'is_staff', 'is_active', 'is_doctor', 'is_superuser')}
			),
		)


admin.site.register(User, UserAdminConfig)