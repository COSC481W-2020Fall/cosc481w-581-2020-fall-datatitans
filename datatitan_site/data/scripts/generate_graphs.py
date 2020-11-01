import matplotlib
import matplotlib.pyplot as plt
import mpld3
from data.models import CovidDataClean, Country, Months, CovidDataMonthly
from django.core.cache import cache
import numpy as np

matplotlib.use('Agg')
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


def gen_graph(*iso_codes, category: str, chart_type: str = "LINE", metric: str = "raw") -> str:
    """Creates a graph that tracks a data category over time for an arbitrary number of countries.

    :param iso_codes: ISO codes of countries to create graphs for
    :param category: The category of data to track (currently supported categories: total_cases, total_deaths)
    :param chart_type: The type of graph to generate (currently supported graphs: line)
    :param metric: Whether to display raw numbers, or to display the numbers per thousand/million
    :return: HTML string representing the generated graph
    :rtype: str
    """
    if len(iso_codes) == 0:
        return ""
    category_name = f"""{"new" if chart_type.lower() == "bar" else "total"}_{category}"""
    if metric == "per_capita":
        category_name += f"""_per_{"thousand" if category == "tests" else "million"}"""
    plt.subplots(figsize=dims)

    selected_countries = Country.objects.filter(iso_code__in=iso_codes)

    plt.title(
        category_name.replace("_", " ").title()
        + " in "
        + ", ".join(
            cache.get_or_set(
                f"country_name_{code}", selected_countries.get(iso_code=code).name
            )
            if not (country_name := cache.get(f"country_name_{code}"))
            else country_name
            for code in iso_codes
        )
    )
    if chart_type.lower() == "line":
        # Fairly simple implementation
        for code in iso_codes:
            if not (target_query := cache.get(f"query_{code}_{category_name}_{chart_type}")):
                target_query = cache.get_or_set(
                    f"query_{code}_{category_name}_{chart_type}",
                    CovidDataClean.objects.filter(iso_code__exact=code).order_by(
                        "date"
                    ),
                )
            # if code == "USA":  # quick fix for USA total cases padding issue on Y axis
            #     plt.ylabel(category_name[category], labelpad=36)
            plt.plot(
                target_query.values_list("date"),
                target_query.values_list(category_name),
                label=code,
            )
    elif chart_type.lower() == "bar":
        # This was an absolute nightmare to figure out
        if not (months := cache.get("months")):
            months = cache.get_or_set(
                "months", Months.objects.filter(month__gte="2020-01-01")
            )
        offset_y = np.zeros(
            months.count()
        )  # A numpy array that will be used to store the offsets for each bar graph
        # TODO: Find a more graceful way to set the correct category
        for code in iso_codes:
            if not (country_results := cache.get(f"monthly_results_{code}")):
                country_results = cache.get_or_set(
                    f"monthly_results_{code}",
                    CovidDataMonthly.objects.filter(
                        iso_code=code
                    ),
                )
            valid_months = country_results.filter(iso_code=code).dates(
                "month", "month"
            )  # The list of months this country has data for
            current_country = selected_countries.get(iso_code=code)
            if not (target_query := cache.get(f"query_{code}_{category_name}_{chart_type}")):
                target_query = cache.get_or_set(
                    f"query_{code}_{category_name}_{chart_type}",
                    [
                        country_results.values().get(month=month)
                        if months.get(month=month).month in valid_months
                        else {
                            "iso_code": code,
                            "continent": current_country.continent,
                            "location": current_country.name,
                            "month": month,
                            "new_cases": 0,
                            "new_deaths": 0,
                            "new_tests": 0,
                            "new_cases_per_million": 0,
                            "new_deaths_per_million": 0,
                            "new_tests_per_thousand": 0,
                            "data_key": f"{month}{code}",
                        }
                        for month in months.values_list(flat=True)
                    ],
                )
            target_list = [
                float(item[category_name]) for item in target_query
            ]
            plt.bar(
                list(months.values_list(flat=True)),
                target_list,
                bottom=offset_y,
                label=code,
                width=10,
            )
            offset_y += target_list
    plt.legend(shadow=True, fancybox=True, loc=2, prop={"size": 10})
    plt.xlabel("Dates")
    plt.ylabel(category_name.replace("_", " ").title())

    figure = plt.gcf()
    plt.draw()
    graph_output = mpld3.fig_to_html(figure, figid="graph")
    plt.close(figure)
    return graph_output
