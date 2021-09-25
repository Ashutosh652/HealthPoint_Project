from django.db import models
from django.utils import timezone
from account.models import User, ThreadModel
from PIL import Image


class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	image = models.ImageField(upload_to='post_photos', blank=True, null=True)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, blank=True, related_name='likes')
	dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

	class Meta:
		ordering = ['-date_posted']

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	date_commented = models.DateTimeField(default=timezone.now)
	likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
	dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

	@property
	def children(self):
		return Comment.objects.filter(parent=self).order_by('-date_commented').all()

	@property
	def is_parent(self):
		if self.parent is None:
			return True
		return False

	class Meta:
		ordering = ['-date_commented']

	def __str__(self):
		return 'Comment {} by {}'.format(self.content, self.author)


class Notification(models.Model):
	# 1=like, 2=comment, 3=follow, 4-dm
	notification_type = models.IntegerField()
	to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
	from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	user_has_seen = models.BooleanField(default=False)