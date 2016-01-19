from django.conf import settings
from django.http import HttpResponseForbidden
from django.template import RequestContext, loader
from django.utils.importlib import import_module


class Http403(Exception):
    pass


class Http403Middleware(object):

    def process_exception(self, request, exception):

        if not isinstance(exception, Http403):
            return None

        try:
            callback = getattr(import_module(settings.ROOT_URLCONF), 'handler403')
            return callback(request, exception)
        except (ImportError, AttributeError):

            t = loader.get_template('403.html')
            print(exception)

            c = RequestContext(request, {
                'message': exception
            })

            return HttpResponseForbidden(t.render(c))
