from django.shortcuts import render
from django.utils import timezone
from .models import Post


def home(request):
    return render(request, 'data.html', {})


def about(request):
    return render(request, 'about.html', {})


def blog(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog.html', {'posts': posts})

def blog_detail(request, blog_id):
    blog_post = Post.objects.get(pk=blog_id)
    return render(request, 'blog_detail.html', {'post': blog_post})