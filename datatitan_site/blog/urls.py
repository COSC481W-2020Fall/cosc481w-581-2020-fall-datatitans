from django.urls import path

from blog import views

urlpatterns = [
    path("", views.blog, name="blog"),
    path("author/<blog_author>", views.blog_author, name="blog_author"),
    path("detail/<blog_id>", views.blog_detail, name="blog_detail"),
]
