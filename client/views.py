import logging
from django.http import HttpResponse

LOGGER = logging.getLogger(__name__)


def client(request):
    LOGGER.info(f"Hit client with {request.GET}")
    return HttpResponse()
