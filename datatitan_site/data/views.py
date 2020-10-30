# The "view" in django mvc architecture which integrates with html to display data

from django.shortcuts import render
from django.utils import timezone
from data.models import Post, Country, Comment
from data.scripts.generate_graphs import gen_graph
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_GET
from data.forms import ChartSelector, CommentForm
from django.views.decorators.cache import cache_page


@require_GET
@cache_page(60 * 10)
def home(request):
    # Get items from the form
    form = ChartSelector(request.GET)
    if form.is_valid():
        countries = form.cleaned_data["country_code"].values_list("country_code", flat=True)
        data_category = form.cleaned_data["data_type"]
        chart_type = form.cleaned_data["chart_type"]
    else:
        countries = []
        data_category = "TOTAL_CASES"
        chart_type = "LINE"
    countries = list(dict.fromkeys(countries))
    countries = [country for country in countries if country != "none"]
    countries = list(filter(None, countries))
    return render(
        request,
        "data.html",
        {
            "chart": gen_graph(*countries, category=str.lower(data_category), chart_type=chart_type),
            "country_selector": ChartSelector(
                selected_country_codes=countries,
                selected_data_type=data_category,
                selected_chart_type=chart_type,
            ).as_p(),
        },
    )


def about(request):
    return render(request, "about.html", {})


def blog(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog.html", {"posts": posts})


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
    commentForm = CommentForm()
    
    return render(request, "blog_detail.html", {"post": blog_post, "comments": comments, "form": CommentForm})
