# employees/admin.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.core.management import call_command
from .models import Employees, Analytics

@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'path', 'ip_address', 'user_agent')
    list_filter = ('path', 'timestamp')
    search_fields = ('ip_address', 'user_agent', 'path')
    ordering = ('-timestamp',)

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'department')
    change_list_template = "admin/employees_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('run-data-pipeline/', self.admin_site.admin_view(self.run_data_pipeline), name='run-data-pipeline'),
            path('clear-all/', self.admin_site.admin_view(self.clear_all_employees), name='clear-all-employees'),
        ]
        return custom_urls + urls

    def clear_all_employees(self, request):
        Employees.objects.all().delete()
        self.message_user(request, "✅ All employee records deleted.", level=messages.SUCCESS)
        return redirect('..')  # go back to the employee changelist page

    def run_data_pipeline(self, request):
        try:
            call_command('parse_emp')  # your full data pipeline command
            self.message_user(request, "✅ Data pipeline executed successfully.", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"❌ Error running pipeline: {e}", level=messages.ERROR)
        return redirect("..")  # go back to the employee list view

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['custom_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Employees, EmployeesAdmin)
