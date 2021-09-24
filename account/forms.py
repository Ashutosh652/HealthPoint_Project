from django import forms
from .models import User, Doctor, Appointment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from bootstrap_datepicker_plus import DatePickerInput


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(label='Email')
	full_name = forms.CharField(label='Full Name' ,max_length = 100)
	date_of_birth = forms.DateField(label='Date of Birth', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)

	class Meta:
		model = User
		fields = ['full_name', 'user_name', 'email', 'date_of_birth' ,'password1', 'password2']


class DoctorRegisterForm(UserCreationForm):
	email = forms.EmailField(label='Email')
	full_name = forms.CharField(label='Full Name' ,max_length = 100)
	date_of_birth = forms.DateField(label='Date of Birth', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
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

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(label='Email', required=False)
	full_name = forms.CharField(label='Full Name', max_length = 100, required=False)
	user_name = forms.CharField(max_length=20, required=False)

	class Meta:
		model = User
		fields = ['full_name', 'user_name', 'email']


class UserProfileUpdateForm(forms.ModelForm):
	address = forms.CharField(label='Address', max_length = 300, required = False)
	date_of_birth = forms.DateField(label='Date of Birth', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
	profile_pic = forms.ImageField(required=False)

	class Meta:
		model = User
		fields = ['date_of_birth', 'profile_pic', 'address']


class DoctorUpdateForm(forms.ModelForm):
	address = forms.CharField(label='Address', max_length = 300, required = False)
	date_of_birth = forms.DateField(label='Date of Birth', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
	profile_pic = forms.ImageField(required=False)
	college_attended = forms.CharField(label='College Attended' ,max_length = 200, required=False)
	college_address = forms.CharField(label='College Location' ,max_length = 200, required=False)
	date_graduated = forms.DateField(label='Date Graduated', required=False)
	certificate_of_graduation = forms.ImageField(label='Certificate of Graduation', required=False)
	current_affiliation = forms.CharField(label='Current Workplace' ,max_length = 200, required=False)
	specialization = forms.CharField(label='Specialization' ,max_length = 100, required=False)

	class Meta:
		model = Doctor
		fields = ['address','date_of_birth', 'profile_pic', 'college_attended', 'college_address', 'date_graduated', 'certificate_of_graduation', 'current_affiliation', 'specialization']


class AppointmentForm(forms.ModelForm):
	date = forms.DateField(label='Date', widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)
	detail = forms.CharField(label='', widget=forms.Textarea(attrs={'style':'max-width : 40em', 'rows':3, 'placeholder':'Short Description for the Reason of Requesting Appointment.'}), required=True)
	# is_accepted = forms.BooleanField(label='', required=False)
	# is_rejected = forms.BooleanField(label='', required=False)

	class Meta:
		model = Appointment
		fields = ['date', 'detail']


# class AcceptAppointmentForm(forms.ModelForm):
# 	is_accepted = forms.BooleanField(label='Accept')

# 	class Meta:
# 		model = Appointment
# 		fields = ['is_accepted']

# 	@transaction.atomic
# 	def data_save(self):
# 		appointment = self.save(commit=False)
# 		appointment.is_accepted = True
# 		appointment.save()