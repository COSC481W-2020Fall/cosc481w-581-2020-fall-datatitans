import matplotlib.pyplot as plt
import mpld3
from data.models import CovidDataClean, Country

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


def gen_graph(*iso_codes, category: str, chart_type="line") -> str:
    """Creates a graph that tracks a data category over time for an arbitrary number of countries.

    :param iso_codes: ISO codes of countries to create graphs for
    :param category: The category of data to track (currently supported categories: total_cases, total_deaths)
    :param chart_type: The type of graph to generate (currently supported graphs: line)
    :return: HTML string representing the generated graph
    :rtype: str
    """
    if len(iso_codes) == 0:
        return ""
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
