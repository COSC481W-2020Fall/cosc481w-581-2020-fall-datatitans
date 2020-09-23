from django.shortcuts import render
from django.utils import timezone
from .models import Post, Country
from pathlib import Path


def home(request):
    img_url = "static/USA1.jpeg"
    selected_country = "USA"
    selected_data = "Total Cases"
    countries = [("USA", "USA"), ("CAN", "Canada"), ("MEX", "Mexico")]
    data_type = [("TOTAL_CASES", "Total Cases"), ("TOTAL_DEATHS", "Total Deaths")]

    if request.method == "POST":
        # Get items from the form
        # form = ListForm(request.POST or None)
        form = request.POST

        country_code = form["country_code"]
        chart_type = form["data_code"]

        return render(
            request,
            "data.html",
            {
                "chart": Path(f"static/{country_code}{1 if chart_type == 'TOTAL_CASES' else 2}.jpeg"),
                "countries": countries,
                "selected_country": Country.objects.get(country_code=country_code).name,
                "data_type": data_type,
                "selected_data": "Total Cases" if chart_type == "TOTAL_CASES" else "Total Deaths",
            },
        )
    else:

        # chart = seaborn(country_code, chart_type)
        return render(
            request,
            "data.html",
            {
                "chart": img_url,
                "countries": countries,
                "selected_country": selected_country,
                "data_type": data_type,
                "selected_data": selected_data,
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
