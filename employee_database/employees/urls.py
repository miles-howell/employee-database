from django.urls import path
from . import views
from .views import landing_page

urlpatterns = [
    path('', landing_page, name='landing'),
    path('employees/', views.employees, name='employees'),
    path('employees/details/<slug:slug>', views.details, name='details'),
    path('search/', views.search_employees, name='search_employees'),

]