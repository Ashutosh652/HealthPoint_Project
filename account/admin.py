from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, UserProfile, Appointment, ThreadModel, MessageModel

class UserAdminConfig(UserAdmin):
	search_fields = ('user_name', 'email', 'full_name')
	list_filter = ('is_active', 'is_staff', 'is_doctor', 'is_email_verified')
	ordering = ('-date_joined',)
	list_display = ('email', 'user_name', 'full_name', 'is_active', 'is_staff', 'is_doctor')
	fieldsets = (
		(None, {'fields': ('email', 'user_name', 'full_name', 'date_joined',)}),
		('Permissions', {'fields': ('is_staff', 'is_active', 'is_doctor', 'is_superuser', 'is_email_verified')}),
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
admin.site.register(UserProfile)
admin.site.register(Appointment)
admin.site.register(ThreadModel)
admin.site.register(MessageModel)