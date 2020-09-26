import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mpld3
from ..models import CovidDataClean, Country
import sqlite3
from datatitan_site.settings import DATABASES

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
    plt.title(category_name[category] + " in " + Country.objects.get(country_code=iso_code).name)
    with sqlite3.connect(DATABASES["default"]["NAME"]) as conn:
        df = pd.read_sql(f"""select date, {category} from data_coviddataclean""", con=conn)
    a = sns.lineplot(data=df, x="date", y=category)
    for ind, label in enumerate(a.get_xticklabels()):
        label.set_visible(ind % 10 == 0)
    plt.xlabel("Dates")
    plt.ylabel(category_name[category])
    plt.xticks(rotation=-45)
    figure = plt.gcf()
    plt.draw()
    graph_output = mpld3.fig_to_html(figure)
    plt.close(figure)
    return graph_output
