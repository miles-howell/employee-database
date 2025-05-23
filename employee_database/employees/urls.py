# Copyright (c) 2025 Miles H. (Planned Pixel Studio)
# Licensed for personal or educational use only.
# Commercial use, redistribution, or resale requires a paid license.
# Contact: miles@plannedpixel.com

from django.urls import path
from . import views
from .views import landing_page

urlpatterns = [
    path('', landing_page, name='landing'),
    path('employees/', views.employees, name='employees'),
    path('employees/details/<slug:slug>', views.details, name='details'),
    path('search/', views.search_employees, name='search_employees'),

]