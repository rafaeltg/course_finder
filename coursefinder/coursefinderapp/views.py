from django.shortcuts import render

from .forms import FilterForm
from .models import Course


def index(request):

    courses = []

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FilterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data

            filters = {}

            selected_countries = data['countries']
            if len(selected_countries) > 0:
                filters['location__country__in'] = selected_countries

            selected_jobs = data['industries']
            if len(selected_jobs) > 0:
                filters['jobs__in'] = selected_jobs

            if len(filters) > 0:
                limit = data['limit']
                courses = Course.objects.filter(**filters).order_by('title')[:limit]

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FilterForm()

    return render(request, 'index.html', {'form': form, 'courses': courses})
