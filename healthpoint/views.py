from django.shortcuts import render
from .models import Post

posts = [
	{'title' : 'Title1',
	'author' : 'User1',
	'date_posted' : 'Date1',
	'content' : 'Context1'},
	{'title' : 'Title2',
	'author' : 'User2',
	'date_posted' : 'Date2',
	'content' : 'Context2'}
]

def home(request):
	content = {
		'posts' : Post.objects.all()
	}
	return render(request, 'healthpoint/home.html', content)

def about(request):
	return render(request, 'healthpoint/about.html')