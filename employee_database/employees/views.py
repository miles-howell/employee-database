# Copyright (c) 2025 Miles H. (Planned Pixel Studio)
# Licensed for personal or educational use only.
# Commercial use, redistribution, or resale requires a paid license.
# Contact: miles@plannedpixel.com

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Employees
from django.db.models import Q, Value
from django.db.models.functions import Concat
import logging
from datetime import datetime, date
import csv

logger = logging.getLogger(__name__)

def landing_page(request):
    today = date.today()
    this_month = today.month

    birthdays = Employees.objects.filter(bday__month=this_month).order_by('bday__day')
    anniversaries = Employees.objects.filter(doh__month=this_month).order_by('doh__day')

    context = {
        'birthdays': birthdays,
        'anniversaries': anniversaries,
        'today': today,
    }

    return render(request, 'landing.html', context)

def employees(request):
    #template = loader.get_template('directory.html')
    today = date.today()
    selected_department = request.GET.get('department')
    departments = Employees.objects.values_list('department', flat=True).distinct()


    if selected_department:
        myEmps = Employees.objects.filter(department=selected_department)
    else:
        myEmps = Employees.objects.all()

    context = {
        'myEmps': myEmps,
        'departments': departments,
        'selected_department': selected_department,
        'today': today,
    }

    return render(request, 'directory.html', context)

def details(request, slug):
    today = date.today()
    myEmp = Employees.objects.get(slug=slug)
    referer = request.META.get('HTTP_REFERER', '/employees')
    template = loader.get_template('details.html')
    context = {
        'myEmp': myEmp,
        'referer': referer,
        'today': today,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def search_employees(request):
    today = date.today()

    # Extract GET parameters
    firstname = request.GET.get('firstname', '').strip()
    lastname = request.GET.get('lastname', '').strip()
    phone = request.GET.get('phone', '').strip()
    department = request.GET.get('department', '').strip()
    title = request.GET.get('title', '').strip()
    doh_start = request.GET.get('doh_start', '').strip()
    doh_end = request.GET.get('doh_end', '').strip()
    head = request.GET.get('head')  # Checkbox
    spv = request.GET.get('spv')    # Checkbox

    date_format = "%Y-%m-%d"

    filters = Q()

    if firstname:
        filters &= Q(firstname__icontains=firstname)
    if lastname:
        filters &= Q(lastname__icontains=lastname)
    if phone:
        filters &= Q(phone__icontains=phone)
    if department:
        filters &= Q(department__icontains=department)
    if title:
        filters &= Q(title__icontains=title)
    if doh_start:
        try:
            start_date = datetime.strptime(doh_start, date_format).date()
            filters &= Q(doh__gte=start_date)
        except ValueError:
            logger.error(f"Invalid start date: {doh_start}")
            pass

    if doh_end:
        try:
            end_date = datetime.strptime(doh_end, date_format).date()
            filters &= Q(doh__lte=end_date)
        except ValueError:
            logger.error(f"Invalid end date: {doh_end}")
            pass
    if head is not None:
        filters &= Q(head=True)
    if spv is not None:
        filters &= Q(spv=True)

    results = Employees.objects.filter(filters)

    if 'firstname' in request.GET:
        results = results.filter(firstname__icontains=request.GET['firstname'])
    if 'lastname' in request.GET:
        results = results.filter(lastname__icontains=request.GET['lastname'])
    # Continue adding filters for other fields

    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employees.csv"'

        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Phone', 'Department', 'Title', 'Date of Hire', 'Head', 'Supervisor'])

        # Debug: Write only the first few results for sanity check
        for emp in results:
            print(f"Writing to CSV: {emp.firstname} {emp.lastname}")  # Debugging line
            writer.writerow([
                emp.firstname or '',
                emp.lastname or '',
                emp.phone or '',
                emp.department or '',
                emp.title or '',
                emp.doh.strftime('%Y-%m-%d') if emp.doh else '',
                'Yes' if emp.head else 'No',
                'Yes' if emp.spv else 'No',
            ])
        return response

    return render(request, 'search_results.html', {
        'results': results,
        'query': request.GET.urlencode(),  # optional — since we're using field-based search now
        'today': today,
    })
