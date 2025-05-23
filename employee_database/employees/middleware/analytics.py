# Copyright (c) 2025 Miles H. (Planned Pixel Studio)
# Licensed for personal or educational use only.
# Commercial use, redistribution, or resale requires a paid license.
# Contact: miles@plannedpixel.com

from employees.models import Analytics

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.path.startswith('/admin'):  # Skip admin page
            try:
                Analytics.objects.create(
                    path=request.path,
                    query_string=request.META.get('QUERY_STRING', ''),
                    ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0'),
                    user_agent=request.META.get('HTTP_USER_AGENT', 'Unknown'),
                )
            except Exception as e:
                # Optional: print or log error if needed
                pass
        max_entries = 10000
        excess = Analytics.objects.count() - max_entries
        if excess > 0:
            # Delete oldest entries (by timestamp)
            Analytics.objects.order_by('timestamp')[:excess].delete()

        return response