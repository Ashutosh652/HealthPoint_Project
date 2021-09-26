from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

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

	def create_user(self, email, user_name, full_name ,password, **other_fields):
		if not email:
			raise ValueError('Users must provide an email.')
		if not user_name:
			raise ValueError('Users must provide a user name.')
		if not full_name:
			raise ValueError('Users must provide a full name.')
		email = self.normalize_email(email)
		user = self.model(email=email, user_name=user_name, full_name=full_name, **other_fields)
		user.set_password(password)
		user.save()


class User(AbstractBaseUser, PermissionsMixin):

	id = models.AutoField(primary_key = True)
	email = models.EmailField(max_length=200, unique=True)
	is_email_verified = models.BooleanField(default=False)
	user_name = models.CharField(max_length=20, unique=True)
	full_name = models.CharField(max_length=100)
	date_joined = models.DateTimeField(default=timezone.now, blank=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_doctor = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	objects = AccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['user_name', 'full_name']

	def __str__(self):
		return self.user_name

	def has_perm(self, perm, obj=None):
		return self.is_staff

	def has_module_perms(self, app_label):
		return self.is_superuser
#....................CUSTOM USER MODEL...........................

class Doctor(models.Model):
	user = models.OneToOneField(User, related_name='doctor' ,on_delete=models.CASCADE, primary_key=True)
	college_attended = models.CharField(max_length=200)
	college_address = models.CharField(max_length=200)
	date_graduated = models.DateField(null=True, blank=True)
	certificate_of_graduation = models.ImageField(upload_to='certificates')
	current_affiliation = models.CharField(max_length=200)
	specialization = models.CharField(max_length=100)
	work_phone = PhoneNumberField(blank=True, null=True, unique=True)

	def __str__(self):
		return self.user.user_name


class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile' ,on_delete=models.CASCADE, primary_key=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	phone = PhoneNumberField(blank=True, null=True, unique=True)
	followers = models.ManyToManyField(User, blank=True, related_name='followers')
	followings = models.ManyToManyField(User, blank=True, related_name='followings')

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.profile_pic.path)
		if img.height>300 or img.width>300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.profile_pic.path)

	def __str__(self):
		return self.user.user_name


class Appointment(models.Model):
	by_user = models.ForeignKey(User, related_name='appointment_by', on_delete=models.CASCADE)
	to_doctor = models.ForeignKey(Doctor, related_name='appointment_to', on_delete=models.CASCADE)
	#preferred date for appointment by by_user
	date = models.DateField()
	detail = models.TextField(null=False, blank=False)
	is_accepted = models.BooleanField(default=False)
	is_rejected = models.BooleanField(default=False)


class ThreadModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')


class MessageModel(models.Model):
	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
	sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	body = models.CharField(max_length=1000)
	image = models.ImageField(upload_to='message_photos', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)