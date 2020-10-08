from django.shortcuts import render
from django.utils import timezone
from data.models import Post, Country
from data.scripts.generate_graphs import gen_graph
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_GET
from data.forms import ChartSelector


@require_GET
def home(request):
    category_name = {"total_cases": "Total Cases", "total_deaths": "Total Deaths"}

    # Get items from the form
    form = request.GET

    try:
        countries = form.getlist("country_code", default=[])
        data_category = form["data_code"]
        chart_type = form["chart_code"]
    except MultiValueDictKeyError:
        countries = ["USA", "none"]
        data_category = "TOTAL_CASES"
        chart_type = "LINE"
    countries = list(dict.fromkeys(countries))
    countries = [country for country in countries if country != "none"]
    countries = list(filter(None, countries))
    return render(
        request,
        "data.html",
        {
            "chart": gen_graph(*countries, category=str.lower(data_category)),
            "countries": Country().country_names,
            "countries2": Country().country_names,
            "selected_country1": Country.objects.get(country_code=countries[0]).name,
            "selected_country2": Country.objects.get(country_code=countries[1]).name
            if len(countries) > 1
            else "none",
            "data_type": [
                (str.upper(raw), category_name[raw]) for raw in category_name
            ],
            "selected_data": category_name[str.lower(data_category)],
            "country_selector": ChartSelector()
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
