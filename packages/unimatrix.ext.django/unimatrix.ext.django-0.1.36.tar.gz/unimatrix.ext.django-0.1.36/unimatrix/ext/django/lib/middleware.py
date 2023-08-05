"""Middleware to report application status to the infrastructure."""
import logging

from django.http import HttpResponse


class HealthCheckMiddleware:
    """Intercepts ``GET`` requests on ``/.well-known/probe/live``
    and ``/.well-known/probe/ready`` to report application health.
    """
    logger = logging.getLogger("probe")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if request.method == "GET":
            if request.path == "/.well-known/probe/ready":
                response = self.ready(request)
            elif request.path == "/.well-known/probe/live":
                response = self.live(request)
        return response or self.get_response(request)

    def live(self, request):
        """Respond with ``200 OK``."""
        self.logger.info("Received liveness probe from %s",
            request.META['REMOTE_ADDR'])
        return HttpResponse("OK")

    def ready(self, request):
        """Respond with ``200 OK`` if all services are operational."""
        self.logger.info("Received readyness probe from %s",
            request.META['REMOTE_ADDR'])
        return HttpResponse("OK")
