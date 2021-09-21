from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.views.generic import RedirectView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Post, Comment, Notification
from account.models import UserProfile, User
from .forms import PostForm, CommentForm


# def home(request):
# 	if request.method == 'POST':
# 		form = PostForm(request.POST, request.FILES, instance=request.user)
# 		if form.is_valid():
# 			form.save()
# 			messages.success(request, f'Your post has been created!')
# 			return redirect('healthpoint-home')
# 	else:
# 		form = PostForm(instance=request.user)

# 	context = {
# 		'posts' : Post.objects.all(),
# 		'form' : form,
# 	}
# 	return render(request, 'healthpoint/home.html', context)

class home(View):
	def get(self, request, *args, **kwargs):
		logged_in_user = request.user
		posts = Post.objects.filter(
			author__profile__followers__in = [logged_in_user.id]
			)
		form = PostForm()

		context = {
		'posts':posts,
		'form': form
		}
		return render(request, 'healthpoint/home.html', context)

	def post(self, request, *args, **kwargs):
		logged_in_user = request.user
		posts = Post.objects.filter(
			author__profile__followers__in = [logged_in_user.id]
			)
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()

		context = {
		'posts':posts,
		'form': form
		}
		return render(request, 'healthpoint/home.html', context)


def about(request):
	return render(request, 'healthpoint/about.html')


class PostDetailView(View):
	def get(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form = CommentForm()
		comments = Comment.objects.filter(post=post)

		context = {
			'post': post,
			'form': form,
			'comments':comments
		}
		return render(request, 'healthpoint/post_detail.html', context)

	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.author = request.user
			new_comment.post = post
			new_comment.save()
		comments = Comment.objects.filter(post=post)

		notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)

		context = {
			'post': post,
			'form': form,
			'comments':comments
		}
		return render(request, 'healthpoint/post_detail.html', context)


class CommentReplyView(LoginRequiredMixin, View):
	def post(self, request, post_pk, pk, *args, **kwargs):
		post = Post.objects.get(pk=post_pk)
		parent_comment = Comment.objects.get(pk=pk)
		form = CommentForm(request.POST)

		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.author = request.user
			new_comment.post = post
			new_comment.parent = parent_comment
			new_comment.save()

		notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment)

		return redirect('post-detail', pk=post_pk)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	template_name = 'healthpoint/post_edit.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('post-detail', kwargs={'pk':pk})

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'healthpoint/post_delete.html'
	success_url = reverse_lazy('healthpoint-home')

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author


class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Comment
	fields = ['content']
	template_name = 'healthpoint/comment_edit.html'

	def get_success_url(self):
		pk = self.kwargs['post_pk']
		return reverse_lazy('post-detail', kwargs={'pk':pk})

	def test_func(self):
		comment = self.get_object()
		return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = 'healthpoint/comment_delete.html'

	def get_success_url(self):
		pk = self.kwargs['post_pk']
		return reverse_lazy('post-detail', kwargs={'pk': pk})

	def test_func(self):
		comment = self.get_object()
		return self.request.user == comment.author


class AddLike(LoginRequiredMixin, RedirectView):
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)

		disliked = False
		for dislike in post.dislikes.all():
			if dislike == request.user:
				disliked = True
				break

		if disliked:
			post.dislikes.remove(request.user)

		liked = False
		for like in post.likes.all():
			if like == request.user:
				liked = True
				break

		if not liked:
			post.likes.add(request.user)
			notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)

		if liked:
			post.likes.remove(request.user)

		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)


class AddDislike(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)

		liked = False
		for like in post.likes.all():
			if like == request.user:
				liked = True
				break

		if liked:
			post.likes.remove(request.user)

		disliked = False
		for dislike in post.dislikes.all():
			if dislike == request.user:
				disliked = True
				break

		if not disliked:
			post.dislikes.add(request.user)

		if disliked:
			post.dislikes.remove(request.user)

		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)


class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        disliked = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                disliked = True
                break

        if disliked:
            comment.dislikes.remove(request.user)

        liked = False

        for like in comment.likes.all():
            if like == request.user:
                liked = True
                break

        if not liked:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)

        if liked:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        liked = False

        for like in comment.likes.all():
            if like == request.user:
                liked = True
                break

        if liked:
            comment.likes.remove(request.user)

        disliked = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                disliked = True
                break

        if not disliked:
            comment.dislikes.add(request.user)

        if disliked:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class UserSearchView(View):
	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('query')
		profile_list = UserProfile.objects.filter(
			Q(user__user_name__icontains=query) |
			Q(user__full_name__icontains=query)
			)
		post_list = Post.objects.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query)
			)

		context = {
			'profile_list': profile_list,
			'post_list': post_list,
			}

		return render(request, 'healthpoint/search.html', context)


class PostNotification(View):
	def get(self, request, notification_pk, post_pk, *args, **kwargs):
		notification = Notification.objects.get(pk=notification_pk)
		post = Post.objects.get(pk=post_pk)
		notification.user_has_seen = True
		notification.save()
		return redirect('post-detail', pk=post_pk)


class FollowNotification(View):
	def get(self, request, notification_pk, profile_pk, *args, **kwargs):
		notification = Notification.objects.get(pk=notification_pk)
		profile = UserProfile.objects.get(pk=profile_pk)
		notification.user_has_seen = True
		notification.save()
		return redirect('user_profile', pk=profile_pk)


class RemoveNotification(View):
	def delete(self, request, notification_pk, *args, **kwargs):
		notification = Notification.objects.get(pk=notification_pk)
		notification.user_has_seen = True
		notification.save()
		return HttpResponse('Success', content_type="text/plain")