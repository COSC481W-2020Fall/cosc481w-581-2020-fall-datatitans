import matplotlib.pyplot as plt
import mpld3
from ..models import CovidDataClean, Country

SMALL_SIZE = 8
SMALLER_SIZE = 3
MEDIUM_SIZE = 15
BIGGER_SIZE = 20

plt.rc("font", size=MEDIUM_SIZE)  # default text sizes
plt.rc("axes", titlesize=MEDIUM_SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=BIGGER_SIZE)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title


def gen_graph(iso_code: str, category: str, chart_type="line"):
    category_name = {"total_cases": "Total Cases", "total_deaths": "Total Deaths"}
    plt.title(
        category_name[category]
        + " in "
        + Country.objects.get(country_code=iso_code).name
    )
    target_query = CovidDataClean.objects.filter(iso_code__exact=iso_code).order_by("date")
    plt.plot(target_query.values_list("date"), target_query.values_list(category))
    plt.xlabel("Dates")
    plt.ylabel(category_name[category])
    figure = plt.gcf()
    plt.draw()
    graph_output = mpld3.fig_to_html(figure)
    plt.close(figure)
    return graph_output
