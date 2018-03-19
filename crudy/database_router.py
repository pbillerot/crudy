import threading
from django.http import Http404

request_cfg = threading.local()

def RouterMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print("RouterMiddleware")
        request_cfg.user = request.user

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware

class DataBaseRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    request = None

    def _multi_db(self):
        # from django.conf import settings
        # if hasattr(request_cfg, 'db'):
        #     if request_cfg.db in settings.DATABASES:
        #         return request_cfg.db
        #     else:
        #         raise Http404
        # else:
        #     return 'default'
        print("_multi_db")
        return "default"

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        # if request_cfg.user:
        #     print(request_cfg.user.username, "connected")

        print ("db_for_read", model._meta.app_label)
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        print ("db_for_write", model._meta.app_label, request_cfg.user)
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        print ("allow_relation", obj1._meta.app_label, obj2._meta.app_label, request_cfg.user)

        # if obj1._meta.app_label == 'auth' or \
        #    obj2._meta.app_label == 'auth':
        #    return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        # print ("allow_migrate", app_label, request_cfg.user)
        return None

def multidb_context_processor(request):
    """
    This context processor will add a db_name to the request.

    Add this to your Django context processors, for example:

    TEMPLATE_CONTEXT_PROCESSORS +=[
        'bananaproject.multidb.multidb_context_processor']
    """
    if hasattr(request, 'SELECTED_DATABASE'):
        return {'db_name': request.SELECTED_DATABASE}
    else:
        return {}