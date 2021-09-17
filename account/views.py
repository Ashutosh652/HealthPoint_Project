from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import UserRegisterForm, DoctorRegisterForm, UserUpdateForm, DoctorUpdateForm, UserProfileUpdateForm
from django.views.generic import CreateView
from .models import User, Doctor, UserProfile
from healthpoint.models import Post

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
	if request.user.is_authenticated:
		return redirect('healthpoint-home')
	else:
		return render(request, 'account/register.html')


def loginpage(request):
	if request.user.is_authenticated:
		return redirect('healthpoint-home')
	else:
		if request.method == 'POST':
			email = request.POST.get('email')
			password = request.POST.get('password')
			user = authenticate(request, username=email, password=password)
			if user is not None and user.is_active:
				login(request ,user)
				messages.success(request, f'Logged In Successfully.')
				return redirect('healthpoint-home')
			elif user is None:
				messages.error(request, 'The email or password is wrong!')
				return redirect('login')
			else:
				messages.error(request, 'Your account is currently inactive!')
				return redirect('login')
		return render(request, 'account/login.html')


def logoutpage(request):
	logout(request)
	return render(request, 'account/logout.html')


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


# @login_required
# def userprofile(request):
# 	return render(request, 'account/user_profile.html')


@login_required
def user_updateprofile(request, pk):
	if request.method == 'POST':
		form1 = UserUpdateForm(request.POST, request.FILES, instance=request.user)
		form2 = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if form1.is_valid() and form2.is_valid():
			form1.save()
			form2.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('user_profile', pk=pk)
	else:
		form1 = UserUpdateForm(instance=request.user)
		form2 = UserProfileUpdateForm(instance=request.user.profile)
	context = {'pk':pk, 'form1':form1, 'form2':form2}
	return render(request, 'account/user_updateprofile.html', context)

@login_required
def doctor_updateprofile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
		d_form = DoctorUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			u_form.save()
			d_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('user_profile', pk=pk)
	else:
		u_form = UserUpdateForm(instance=request.user)
		d_form = DoctorUpdateForm(instance=request.user.doctor)
	context = {'pk':pk, 'u_form':u_form, 'd_form':d_form}
	return render(request, 'account/doctor_updateprofile.html', context)


class UserProfileView(View):
	def get(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		user = profile.user
		posts = Post.objects.filter(author=user).order_by('-date_posted')

		followers = profile.followers.all()
		followings = profile.followings.all()

		if len(followers) == 0:
			is_following = False

		for follower in followers:
			if follower == request.user:
				is_following = True
				break
			else:
				is_following = False

		number_of_followers = len(followers)
		number_of_followings = len(followings)

		context = {
		'user':user,
		'profile':profile,
		'posts':posts,
		'number_of_followers':number_of_followers,
		'number_of_followings':number_of_followings,
		'is_following':is_following,
		}
		return render(request, 'account/user_profile.html', context)


class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		profile.followers.add(request.user)
		request.user.profile.followings.add(profile.user)
		messages.success(self.request, f'Followed {profile.user.user_name} successfully.')
		return redirect('user_profile', pk=profile.pk)


class RemoveFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		profile.followers.remove(request.user)
		request.user.profile.followings.remove(profile.user)
		messages.success(self.request, f'Unfollowed {profile.user.user_name} successfully.')
		return redirect('user_profile', pk=profile.pk)


# class AddFollowing(LoginRequiredMixin, View):
# 	def post(self, request, pk, *args, **kwargs):
# 		profile = UserProfile.objects.get(pk=pk)
# 		request.user.profile.followings.add(profile.user)


class ListFollowers(View):
	def get(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		followers = profile.followers.all()

		context = {
		'profile' : profile,
		'followers' : followers,
		}

		return render(request, 'account/followers_list.html', context)


class ListFollowings(View):
	def get(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		followings = profile.followings.all()

		context = {
		'profile' : profile,
		'followings' : followings,
		}

		return render(request, 'account/followings_list.html', context)