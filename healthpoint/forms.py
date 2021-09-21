from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
	title = forms.CharField(
		label = '',
		widget = forms.Textarea(attrs={
			'style':'max-width : 40em',
			'rows':1,
			'placeholder':'Title here'
			}))


	content = forms.CharField(
		label = '',
		widget = forms.Textarea(attrs={
			'style':'max-width : 40em',
			'rows':3,
			'placeholder':'Content here'
			}))

	image = forms.ImageField(required=False)

	class Meta:
		model = Post
		fields = ['title', 'content', 'image']


class CommentForm(forms.ModelForm):
	content = forms.CharField(
		label = '',
		widget = forms.Textarea(attrs={
			'style':'max-width : 20em',
			'rows':3,
			'placeholder':'Comment here'
			}))

	class Meta:
		model = Comment
		fields = ['content']