from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', include('coursefinderapp.urls')),
    path('admin/', admin.site.urls),
]