from django import forms
from data.models import Country
from django.core.cache import cache


class CountrySelect(forms.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        self.selected_countries = None
        super(CountrySelect, self).__init__(*args, **kwargs)
        self.attrs["class"] = "custom-checkbox"

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value:
            option["label"] = value.instance.name
            if value.instance.country_code in self.selected_countries:
                option["attrs"]["checked"] = True
        return option


class MemorizedSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        self.selected_option = None
        super(MemorizedSelect, self).__init__(*args, **kwargs)
        self.attrs["class"] = "custom-select form-control"

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        return super().create_option(
            name, value, label, value == self.selected_option, index, subindex, attrs
        )


class ChartSelector(forms.Form):
    chart_type = forms.ChoiceField(
        choices=(("LINE", "Line Chart"), ("BAR", "Bar Graph")), widget=MemorizedSelect
    )
    country_code = forms.ModelMultipleChoiceField(
        (
            cache.get_or_set("countries", Country.objects.all())
            if not (countries := cache.get("countries"))
            else countries
        ),
        widget=CountrySelect,
    )
    data_type = forms.ChoiceField(
        choices=(("TOTAL_CASES", "Total Cases"), ("TOTAL_DEATHS", "Total Deaths")),
        widget=MemorizedSelect,
    )

    def __init__(self, *args, **kwargs):
        selected_countries = kwargs.pop("selected_country_codes", None)
        selected_data_type = kwargs.pop("selected_data_type", None)
        selected_chart_type = kwargs.pop("selected_chart_type", None)
        super(ChartSelector, self).__init__(*args, **kwargs)
        self.fields["country_code"].widget.selected_countries = selected_countries
        self.fields["data_type"].widget.selected_option = selected_data_type
        self.fields["chart_type"].widget.selected_option = selected_chart_type
