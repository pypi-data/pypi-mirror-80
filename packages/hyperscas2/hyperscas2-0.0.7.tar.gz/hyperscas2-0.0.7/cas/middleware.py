"""CAS authentication middleware"""

import logging

from django.conf import settings
from django.contrib.auth import logout as do_logout
from django.http import HttpResponseRedirect
import traceback
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from .exceptions import CasTicketException
from .domain import Domain

logger = logging.getLogger('default')

__all__ = ['CASMiddleware']


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CASMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """Checks that the authentication middleware is installed"""
        request.domain = Domain.filter(request.get_host())

        error = ("The Django CAS middleware requires authentication "
                 "middleware to be installed. Edit your MIDDLEWARE_CLASSES "
                 "setting to insert 'django.contrib.auth.middleware."
                 "AuthenticationMiddleware'.")
        assert hasattr(request, 'user'), error
        if request.domain is None:
            print(f'cas_domain表未匹配到{request.get_host()}')

    def process_exception(self, request, exception):
        """When we get a CasTicketException, that is probably caused by the ticket timing out.
        So logout/login and get the same page again."""
        if isinstance(exception, CasTicketException):
            do_logout(request)
            # This assumes that request.path requires authentication.
            return HttpResponseRedirect(request.path)
        else:
            logger.error(traceback.format_exc())
            return None
