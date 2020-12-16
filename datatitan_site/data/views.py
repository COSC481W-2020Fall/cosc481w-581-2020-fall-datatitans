# The "view" in django mvc architecture which integrates with html to display data

from django.shortcuts import render
from data.models import Country
from data.scripts.generate_graphs import gen_graph
from django.views.decorators.http import require_GET
from data.forms import ChartSelector
from django.views.decorators.cache import cache_page
from django.db.models import F
from django.views import View
import pandas as pd
import numpy as np
import os
import mpld3


@require_GET
@cache_page(60 * 10)
def data(request):
    # Get items from the form
    form = ChartSelector(request.GET)
    if form.is_valid():
        countries = form.cleaned_data["iso_code"].values_list("iso_code", flat=True)
        data_category = form.cleaned_data["data_type"]
        chart_type = form.cleaned_data["chart_type"]
        metric = form.cleaned_data["metric"]
    else:
        countries = []
        data_category = "TOTAL_CASES"
        chart_type = "LINE"
        metric = "raw"
    countries = list(dict.fromkeys(countries))
    countries = [country for country in countries if country != "none"]
    countries = list(filter(None, countries))
    table_fields = (
        "location",
        "population",
        "total_cases",
        "total_deaths",
        "total_tests",
        "total_cases_per_million",
        "total_deaths_per_million",
        "total_tests_per_thousand",
    )
    country_stats = (
        Country.objects.order_by("iso_code")
        .filter(iso_code__in=countries)
        .values_list("name", "population")
        .annotate(
            total_cases=F("countrystats__total_cases"),
            total_deaths=F("countrystats__total_deaths"),
            total_tests=F("countrystats__total_tests"),
            total_cases_per_million=F("countrystats__total_cases")
            / F("population")
            * 1000000,
            total_deaths_per_million=F("countrystats__total_deaths")
            / F("population")
            * 1000000,
            total_tests_per_thousand=F("countrystats__total_tests")
            / F("population")
            * 1000,
        )
    )
    return render(
        request,
        "data/data.html",
        {
            "chart": gen_graph(
                *countries,
                category=str.lower(data_category),
                chart_type=chart_type,
                metric=metric,
            ),
            "country_selector": form.as_p(),
            "fields": (field.replace("_", " ").title() for field in table_fields),
            "country_table": country_stats,
        }
        if form.is_valid()
        else {
            "chart": "",
            "country_selector": ChartSelector().as_p(),
            "fields": table_fields,
            "country_table": None,
        },
    )


class CovidDataView(View):
    template_name = "data/data.html"

    country_names = (
        pd.read_parquet(os.environ["INPUT_FILE"], columns=["location"])
        .droplevel("date")
        .drop_duplicates()
    )

    table_columns = (
        "location",
        "population",
        "total_cases",
        "total_deaths",
        "total_tests",
        "total_cases_per_million",
        "total_deaths_per_million",
        "total_tests_per_thousand",
    )

    def get(self, request, *args, **kwargs):
        form = ChartSelector(request.GET)
        if form.is_valid():
            countries = form.cleaned_data["iso_code"].values_list("iso_code", flat=True)
            data_category: str = form.cleaned_data["data_type"].lower()
            chart_type = form.cleaned_data["chart_type"].lower()
            metric = form.cleaned_data["metric"].lower()
            category_name = f"""{"new" if chart_type.lower() == "bar" else "total"}_{data_category.lower()}"""
            if metric == "normalized":
                category_name += (
                    f"""_per_{"thousand" if data_category == "tests" else "million"}"""
                )
            df: pd.DataFrame = pd.read_parquet(
                os.environ["INPUT_FILE"],
                columns=list(np.unique([*self.table_columns, category_name])),
            ).loc[list(countries)]
            country_stats: pd.DataFrame = (
                df[list(self.table_columns)]
                .groupby(level="iso_code", observed=True)
                .last()
                .copy()
            )
            df = df[[category_name]]
            df = df.loc[df.index.dropna()]
            title = (
                category_name.replace("_", " ").title()
                + " in "
                + ", ".join(self.country_names.loc[list(countries)]["location"])
            )
            if chart_type == "bar":
                df = (
                    df.groupby(
                        [
                            pd.Grouper(level="iso_code"),
                            pd.Grouper(level="date", freq="M"),
                        ],
                        observed=True,
                    )
                    .sum()
                    .unstack(level="iso_code")
                    .droplevel(axis=1, level=0)
                )
                graph_options = {"kind": "bar", "stacked": True, "xlabel": "Month"}
            else:
                df = df.unstack(level="iso_code").droplevel(axis=1, level=0)
                graph_options = {"kind": "line"}
            return render(
                request,
                self.template_name,
                {
                    "chart": mpld3.fig_to_html(
                        df.plot(
                            title=title,
                            ylabel=data_category.capitalize(),
                            **graph_options,
                        ).figure
                    ),
                    "country_selector": form.as_p(),
                    "country_table": country_stats.to_html(),
                },
            )
        else:
            return render(
                request,
                self.template_name,
                {
                    "country_selector": ChartSelector().as_p(),
                },
            )

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def testing_map(request):
    return render(request, "data/testing_map.html", {})


def about(request):
    return render(request, "base/about.html", {})
