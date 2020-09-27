from django.shortcuts import render
from django.utils import timezone
from .models import Post, Country
from pathlib import Path
from .scripts.generate_graphs import gen_graph
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_GET


@require_GET
def home(request):
    category_name = {"total_cases": "Total Cases", "total_deaths": "Total Deaths"}

    # Get items from the form
    # form = ListForm(request.POST or None)
    form = request.GET

    try:
        country_code = form["country_code"]
        data_category = form["data_code"]
        chart_type = form["chart_code"]
    except MultiValueDictKeyError:
        country_code = "USA"
        data_category = "TOTAL_CASES"
        chart_type = "LINE"
    return render(
        request,
        "data.html",
        {
            "chart": gen_graph(
                iso_code=country_code, category=str.lower(data_category)
            ),
            "countries": Country().country_names,
            "selected_country": Country.objects.get(country_code=country_code).name,
            "data_type": [(str.upper(raw), category_name[raw]) for raw in category_name],
            "selected_data": category_name[str.lower(data_category)],
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
    blog_post = Post.objects.get(pk=blog_id)
    return render(request, "blog_detail.html", {"post": blog_post})
