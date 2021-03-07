from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

#....................CUSTOM USER MODEL...........................
class AccountManager(BaseUserManager):

	def create_superuser(self, email, user_name, full_name, password, **other_fields):
		other_fields.setdefault('is_staff', True)
		other_fields.setdefault('is_superuser', True)
		other_fields.setdefault('is_active', True)
		if other_fields.get('is_staff') is not True:
			raise ValueError('Superuser must be assigned to is_staff=True')
		if other_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must be assigned to is_superuser=True')
		return self.create_user(email, user_name, full_name, password, **other_fields)

	def create_user(self, email, user_name, full_name, password, **other_fields):
		email = self.normalize_email(email)
		user = self.model(email=email, user_name=user_name, full_name=full_name, **other_fields)
		user.set_password(password)
		user.save()


class User(AbstractBaseUser, PermissionsMixin):

	id = models.AutoField(primary_key = True)
	email = models.EmailField(max_length=200, unique=True)
	user_name = models.CharField(max_length=20, unique=True)
	full_name = models.CharField(max_length=100)
	date_joined = models.DateTimeField(default=timezone.now)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_doctor = models.BooleanField(default=False)

	objects = AccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['user_name', 'full_name']

	def __str__(self):
		return self.user_name
#....................CUSTOM USER MODEL...........................


class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title
	