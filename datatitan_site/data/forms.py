from django import forms
from data.models import Country
from blog.models import Comment
from django.core.cache import cache


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("username", "text")


class CountrySelect(forms.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        # self.selected_countries = []
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
            # if value.instance.iso_code in self.selected_countries:
            #     option["attrs"]["checked"] = True
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
        choices=(("LINE", "Line Chart"), ("BAR", "Bar Graph")),
        widget=forms.Select(attrs={"class": "custom-select form-control"}),
    )
    iso_code = forms.ModelMultipleChoiceField(
        Country.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "custom-checkbox"}),
        label="Country:",
    )
    data_type = forms.ChoiceField(
        choices=(("CASES", "Cases"), ("DEATHS", "Deaths"), ("TESTS", "Tests")),
        widget=forms.Select(attrs={"class": "custom-select form-control"}),
    )
    metric = forms.ChoiceField(
        choices=(("raw", "Raw"), ("per_capita", "Per Capita")),
        widget=forms.Select(attrs={"class": "custom-select form-control"}),
    )

    # def __init__(self, *args, **kwargs):
    #     selected_countries = kwargs.pop("selected_iso_codes", [])
    #     selected_data_type = kwargs.pop("selected_data_type", None)
    #     selected_chart_type = kwargs.pop("selected_chart_type", None)
    #     super(ChartSelector, self).__init__(*args, **kwargs)
    #     self.fields["iso_code"].widget.selected_countries = selected_countries
    #     self.fields["data_type"].widget.selected_option = selected_data_type
    #     self.fields["chart_type"].widget.selected_option = selected_chart_type
