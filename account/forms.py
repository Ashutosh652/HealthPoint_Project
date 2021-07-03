from django import forms
from .models import User, Doctor
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(label='Email')
	full_name = forms.CharField(label='Full Name' ,max_length = 100)
	date_of_birth = forms.DateField(label='Date of Birth', widget=forms.widgets.DateInput(attrs={'type': 'date'}))

	class Meta:
		model = User
		fields = ['full_name', 'user_name', 'email', 'date_of_birth' ,'password1', 'password2']


class DoctorRegisterForm(UserCreationForm):
	email = forms.EmailField(label='Email')
	full_name = forms.CharField(label='Full Name' ,max_length = 100)
	date_of_birth = forms.DateField(label='Date of Birth', widget=forms.widgets.DateInput(attrs={'type': 'date'}))
	college_attended = forms.CharField(label='College Graduated From' ,max_length=200)
	college_address = forms.CharField(label='Address of College' ,max_length=200)
	date_graduated = forms.DateField(label='Date Graduated', widget=forms.widgets.DateInput(attrs={'type': 'date'}))
	certificate_of_graduation = forms.ImageField(label='Certificate of Graduation')
	current_affiliation = forms.CharField(label='Current Affiliation (eg. Hospital, Clinic, etc.)' ,max_length=200)
	specialization = forms.CharField(label='Specialization' ,max_length=100)

	class Meta(UserCreationForm.Meta):
		model = User
		fields = ['full_name', 'user_name', 'email', 'date_of_birth' ,'password1', 'password2', 'college_attended', 'college_address', 'date_graduated', 'certificate_of_graduation' ,'current_affiliation', 'specialization']

	@transaction.atomic
	def data_save(self):
		user = super().save(commit=False)
		user.is_doctor = True
		user.is_active = False
		user.email = self.cleaned_data.get('email')
		user.full_name = self.cleaned_data.get('full_name')
		user.date_of_birth = self.cleaned_data.get('date_of_birth')
		user.save()
		doctor = Doctor.objects.create(user=user)
		doctor.college_attended = self.cleaned_data.get('college_attended')
		doctor.college_address = self.cleaned_data.get('college_address')
		doctor.date_graduated = self.cleaned_data.get('date_graduated')
		doctor.certificate_of_graduation = self.cleaned_data.get('certificate_of_graduation')
		doctor.current_affiliation = self.cleaned_data.get('current_affiliation')
		doctor.specialization = self.cleaned_data.get('specialization')
		doctor.save()
		return user
