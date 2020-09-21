from django.shortcuts import render
from django.utils import timezone
from .models import Post


def home(request):
    img_url = "static/USA1.jpeg"
    if request.method == 'POST':
        #Get items from the form
        #form = ListForm(request.POST or None)
        form = request.POST
        
        country_code = form['country_code']
        chart_type = form['data_code']
        print(country_code, chart_type)
        
        if(country_code == 'USA'):
            if(chart_type== 'total_deaths'):
                img_url = 'static/USA1.jpeg'
            else:
                img_url = 'static/USA2.jpeg'
        elif(country_code == 'MEX'):
            if(chart_type== 'total_deaths'):
                img_url = 'static/MEX1.jpeg'
            else:
                img_url = 'static/MEX2.jpeg'
        else:
            if(chart_type== 'total_deaths'):
                img_url = 'static/CAN1.jpeg'
            else:
                img_url = 'static/CAN2.jpeg'
        
        return render( request, 'data.html', {'chart': img_url})
    else:
        #get default chart
        country_code = 'USA'
        chart_type = 'total_cases'

        #chart = seaborn(country_code, chart_type)
        return render(request, 'data.html', {'chart': img_url})


def about(request):
    return render(request, 'about.html', {})


def blog(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog.html', {'posts': posts})


def blog_detail(request, blog_id):
    blog_post = Post.objects.get(pk=blog_id)
    return render(request, 'blog_detail.html', {'post': blog_post})
