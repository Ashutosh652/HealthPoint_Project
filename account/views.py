from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, DoctorRegisterForm
from django.views.generic import CreateView
from .models import User, Doctor

# def register(request):
# 	if request.method == 'POST':
# 		form = UserRegisterForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			user_name = form.cleaned_data.get('user_name')
# 			messages.success(request, f'Account created for {user_name}! You can login now!')
# 			return redirect('healthpoint-home')
# 	else:
# 		form = UserRegisterForm()
# 	return render(request, 'account/register.html', {'form': form})

def register(request):
	return render(request, 'account/register.html')


class UserRegister(CreateView):
	model = User
	form_class = UserRegisterForm
	template_name = 'account/user_register.html'

	def form_valid(self, form):
		if self.request.method == 'POST':
			if form.is_valid():
				form.save()
				user_name = form.cleaned_data.get('user_name')
				messages.success(self.request, f'Account created for {user_name}! You can login now!')
				return redirect('login')
		else:
			form = UserRegisterForm()
		return render(self.request, 'account/user_register.html', {'form': form})


class DoctorRegister(CreateView):
	model = User
	form_class = DoctorRegisterForm
	template_name = 'account/doctor_register.html'

	def form_valid(self, form):
		if self.request.method == 'POST':
			if form.is_valid():
				# form.save()
				form.data_save()
				user_name = form.cleaned_data.get('user_name')
				messages.success(self.request, f'Account created for {user_name}! You cannot login until your credentials are verified. This may take upto 24 hours. You will be notified via email after your account is activated.')
				return redirect('healthpoint-home')
		else:
			form = DoctorRegisterForm()
		return render(self.request, 'account/doctor_register.html', {'form': form})


@login_required
def profile(request):
	return render(request, 'account/profile.html')