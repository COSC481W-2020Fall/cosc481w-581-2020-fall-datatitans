from django.shortcuts import render, redirect
from django.utils import timezone
from blog.models import Post, Comment
from blog.forms import CommentForm


# Create your views here.


def blog(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog/blog.html", {"posts": posts})


def blog_detail(request, blog_id):
    blog_post = Post.objects.get(pk=blog_id)

    if request.user.is_authenticated and request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                text=form.cleaned_data.get("text"),
                blog=blog_post,
            )
            return redirect("blog_detail", blog_id=blog_id)

    return render(
        request,
        "blog/blog_detail.html",
        {
            "post": blog_post,
            "comments": blog_post.comment_set.values("user__username", "text"),
            "form": CommentForm(),
        },
    )
