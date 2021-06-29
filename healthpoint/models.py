from django.db import models
from django.utils import timezone
from account.models import User

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-date_posted']

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	date_commented = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['-date_commented']

	def __str__(self):
		return 'Comment {} by {}'.format(self.content, self.author)