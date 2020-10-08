from django import forms
from data.models import Country


class CountrySelect(forms.CheckboxSelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['label'] = value.instance.name
        return option


class ChartSelector(forms.Form):
    country_code = forms.ModelMultipleChoiceField(Country.objects.all(), widget=CountrySelect)
    data_type = forms.Select(choices=["total_cases", "total_deaths"])
    chart_type = forms.Select(choices=["line", "bar"])
