from django.shortcuts import render
from django.utils import timezone
from .models import Post
from pathlib import Path


def home(request):
    img_url = "static/USA1.jpeg"
    selected_country = 'USA'
    selected_data = 'Total Cases'
    countries = [('USA', 'USA'), ('CAN', 'Canada'), ('MEX', 'Mexico')]
    data_type = [('TOTAL_CASES', 'Total Cases'),('TOTAL_DEATHS', 'Total Deaths')]

    if request.method == 'POST':
        #Get items from the form
        #form = ListForm(request.POST or None)
        form = request.POST

        country_code = form['country_code']
        chart_type = form['data_code']
        print(country_code, chart_type)

        if(chart_type == 'TOTAL_CASES'):
            selected_data = 'Total Cases'
        else:
            selected_data = 'Total Deaths'    

        if(country_code == 'USA'):
            if(chart_type== 'TOTAL_DEATHS'):
                img_url = 'static/USA1.jpeg'
            else:
                img_url = 'static/USA2.jpeg'
            selected_country = 'USA'
        elif(country_code == 'MEX'):
            if(chart_type== 'TOTAL_DEATHS'):
                img_url = 'static/MEX1.jpeg'
            else:
                img_url = 'static/MEX2.jpeg'
            selected_country = 'Mexico'
        else:
            if(chart_type== 'TOTAL_CASES'):
                img_url = 'static/CAN1.jpeg'
            else:
                img_url = 'static/CAN2.jpeg'
            selected_country = 'Canada'    
        
        return render( request, 'data.html', {'chart': img_url, 'countries':countries, 'selected_country':selected_country, 'data_type': data_type, 'selected_data': selected_data})
    else:

        #chart = seaborn(country_code, chart_type)
        return render(request, 'data.html', {'chart': img_url, 'countries':countries, 'selected_country':selected_country, 'data_type': data_type, 'selected_data': selected_data})


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
