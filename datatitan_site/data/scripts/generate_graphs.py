# generate_graphs.py uses the gen_graph function to create an image of a chart based on country codes (iso), category, and chart_type.
# At this point, chart type is not needed as line chart is the only option
# It can take a limitless number of country inputs
# the gen_graph function is called from the views file.

import matplotlib.pyplot as plt
import mpld3
from ..models import CovidDataClean, Country

SMALL_SIZE = 10
SMALLER_SIZE = 3
MEDIUM_SIZE = 20
BIGGER_SIZE = 30

plt.rc("font", size=MEDIUM_SIZE)  # default text sizes
plt.rc("axes", titlesize=MEDIUM_SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=BIGGER_SIZE)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title

dims = (8, 4)  # dimension variable for plot area


def gen_graph(*iso_codes, category: str, chart_type="line"):
    category_name = {"total_cases": "Total Cases", "total_deaths": "Total Deaths"}
    plt.subplots(figsize=dims)

    plt.title(
        category_name[category]
        + " in "
        + ", ".join(Country.objects.get(country_code=code).name for code in iso_codes)
    )
    for code in iso_codes:
        target_query = CovidDataClean.objects.filter(iso_code__exact=code).order_by("date")
        plt.plot(target_query.values_list("date"), target_query.values_list(category), label=code)
    plt.legend(shadow=True, fancybox=True, loc=2, prop={'size': 10})
    plt.xlabel("Dates")
    plt.ylabel(category_name[category])

    figure = plt.gcf()
    plt.draw()
    graph_output = mpld3.fig_to_html(figure)
    plt.close(figure)
    return graph_output
