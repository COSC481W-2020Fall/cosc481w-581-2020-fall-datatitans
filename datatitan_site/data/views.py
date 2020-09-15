from django.shortcuts import render

def home(request):
    return render(request, 'data.html', {})

def about(request):
    return render(request, 'about.html', {})

def blog(request):
    return render(request, 'blog.html', {})