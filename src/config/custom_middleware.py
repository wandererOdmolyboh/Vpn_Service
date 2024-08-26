from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound


class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Resource not found")
        except Exception as e:
            return HttpResponse("An error occurred: " + str(e))
