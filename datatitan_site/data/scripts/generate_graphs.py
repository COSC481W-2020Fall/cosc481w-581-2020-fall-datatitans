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


def gen_graph(iso_code1: str, iso_code2: str, category: str, chart_type="line"):
    category_name = {"total_cases": "Total Cases", "total_deaths": "Total Deaths"}
    plt.subplots(figsize=dims)

    if iso_code2 == "none" or iso_code1 == iso_code2:
        plt.title(
            category_name[category]
            + " in "
            + Country.objects.get(country_code=iso_code1).name
        )
        target_query = CovidDataClean.objects.filter(iso_code__exact=iso_code1).order_by("date")
        plt.plot(target_query.values_list("date"), target_query.values_list(category), label=iso_code1)
        plt.legend(shadow=True, fancybox=True, loc=2, prop={'size': 10})
        plt.xlabel("Dates")

        if iso_code1 == "USA" and category == "total_cases":
            plt.ylabel(category_name[category], labelpad=36)
        else:
            plt.ylabel(category_name[category])

        figure = plt.gcf()
        #plt.draw()
        graph_output = mpld3.fig_to_html(figure)
        plt.close(figure)
        return graph_output
    elif iso_code2 is not "none":
        plt.title(
            category_name[category]
            + " in "
            + Country.objects.get(country_code=iso_code1).name
            + " & "
            + Country.objects.get(country_code=iso_code2).name
        )
        target_query = CovidDataClean.objects.filter(iso_code__exact=iso_code1).order_by("date")
        plt.plot(target_query.values_list("date"), target_query.values_list(category), label=iso_code1)
        target_query = CovidDataClean.objects.filter(iso_code__exact=iso_code2).order_by("date")
        plt.plot(target_query.values_list("date"), target_query.values_list(category), label=iso_code2)

        plt.legend(shadow=True, fancybox=True, loc=2, prop={'size': 10})
        plt.xlabel("Dates")

        if iso_code1 == "USA" and category == "total_cases":
            plt.ylabel(category_name[category], labelpad=36)
        else:
            plt.ylabel(category_name[category])

        figure = plt.gcf()
        # plt.draw()
        graph_output = mpld3.fig_to_html(figure)
        plt.close(figure)
        return graph_output
    else:
        plt.title(
            category_name[category]
            + " in "
            + Country.objects.get(country_code=iso_code1).name
        )
        target_query = CovidDataClean.objects.filter(iso_code__exact=iso_code1).order_by("date")
        plt.plot(target_query.values_list("date"), target_query.values_list(category), label=iso_code1)
        plt.legend(shadow=True, fancybox=True, loc=2, prop={'size': 10})
        plt.xlabel("Dates")

        if iso_code1 == "USA" and category == "total_cases":
            plt.ylabel(category_name[category], labelpad=36)
        else:
            plt.ylabel(category_name[category])

        figure = plt.gcf()
        # plt.draw()
        graph_output = mpld3.fig_to_html(figure)
        plt.close(figure)
        return graph_output
