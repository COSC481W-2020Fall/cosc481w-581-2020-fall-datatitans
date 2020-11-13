from django.shortcuts import render
from django.utils import timezone
from blog.models import Post, Comment
from data.forms import CommentForm

# Create your views here.


def blog(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog/blog.html", {"posts": posts})


def blog_detail(request, blog_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = request.username
            comment.text = request.text
            comment.created_date = timezone.now()
            comment.blog_id = blog_id
            comment.save()
    blog_post = Post.objects.get(pk=blog_id)
    comments = Comment.objects.get(blog_id=blog_id)

    return render(
        request,
        "blog/blog_detail.html",
        {"post": blog_post, "comments": comments, "form": CommentForm()},
    )
