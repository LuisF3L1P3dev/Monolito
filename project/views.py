from django.http import JsonResponse
from django.views.generic import View

class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "UP"})
