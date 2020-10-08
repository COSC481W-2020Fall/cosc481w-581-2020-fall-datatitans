from django import forms
from data.models import Country


class CountrySelect(forms.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        self.selected_countries = None
        super(CountrySelect, self).__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['label'] = value.instance.name
            if value.instance.country_code in self.selected_countries:
                option["attrs"]["checked"] = True
        return option


class ChartSelector(forms.Form):
    country_code = forms.ModelMultipleChoiceField(Country.objects.all(), widget=CountrySelect)
    data_type = forms.Select(choices=["total_cases", "total_deaths"])
    chart_type = forms.Select(choices=["line", "bar"])

    def __init__(self, *args, **kwargs):
        selected_countries = kwargs.pop("selected_country_codes", None)
        super(ChartSelector, self).__init__(*args, **kwargs)
        self.fields["country_code"].widget.selected_countries = selected_countries
