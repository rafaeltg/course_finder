from django import forms

from .models import Job, COUNTRY_CHOICES


class FilterForm(forms.Form):
    industries = forms.ModelMultipleChoiceField(
        queryset=Job.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    countries = forms.MultipleChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    limit = forms.IntegerField(
        min_value=1,
        max_value=1000,
        initial=100,
        required=False,
    )
