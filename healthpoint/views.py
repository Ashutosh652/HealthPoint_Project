from django.shortcuts import render
from django.http import HttpResponse

posts = [
	{'title' : 'Title1',
	'postedby' : 'User1',
	'date' : 'Date1',
	'context' : 'Context1'},
	{'title' : 'Title2',
	'postedby' : 'User2',
	'date' : 'Date2',
	'context' : 'Context2'}
]

def home(request):
	content = {
		'posts' : posts
	}
	return render(request, 'healthpoint/home.html', content)

def about(request):
	return render(request, 'healthpoint/about.html')