from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor

class UserAdminConfig(UserAdmin):
	search_fields = ('user_name', 'email', 'full_name')
	list_filter = ('is_active', 'is_staff', 'is_doctor')
	ordering = ('-date_joined',)
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

class DoctorAdmin(admin.ModelAdmin):
	search_fields = ('user__user_name', 'specialization' ,'college_attended', 'current_affiliation')
	list_display = ('user', 'specialization' ,'college_attended', 'current_affiliation')


admin.site.register(User, UserAdminConfig)
admin.site.register(Doctor, DoctorAdmin)