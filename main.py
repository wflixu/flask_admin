import os

os.environ['PGADMIN_SERVER_MODE'] = 'OFF'
os.environ['PGADMIN_INT_KEY'] = '6217b349-4000-433e-a008-e1dacfdd7a8b'
os.environ['PGADMIN_INT_PORT'] = '5050'

import sys
import builtins


builtins.SERVER_MODE = True


import config
import setup

from pgadmin import create_app, socketio

from pgadmin.utils.constants import INTERNAL

from pgadmin.model import SCHEMA_VERSION



##########################################################################
# Support reverse proxying
##########################################################################
class ReverseProxied():
    def __init__(self, app):
        self.app = app
        # https://werkzeug.palletsprojects.com/en/0.15.x/middleware/proxy_fix
        try:
            from werkzeug.middleware.proxy_fix import ProxyFix
            self.app = ProxyFix(app,
                                x_for=config.PROXY_X_FOR_COUNT,
                                x_proto=config.PROXY_X_PROTO_COUNT,
                                x_host=config.PROXY_X_HOST_COUNT,
                                x_port=config.PROXY_X_PORT_COUNT,
                                x_prefix=config.PROXY_X_PREFIX_COUNT
                                )
        except ImportError:
            pass

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
        if script_name:
            environ["SCRIPT_NAME"] = script_name
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO"] = path_info[len(script_name):]
        scheme = environ.get("HTTP_X_SCHEME", "")
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return self.app(environ, start_response)


##########################################################################
# Sanity checks
##########################################################################
config.SETTINGS_SCHEMA_VERSION = SCHEMA_VERSION


# Check if the database exists. If it does not, create it.
setup_db_required = False
if not os.path.isfile(config.SQLITE_PATH):
    setup_db_required = True

print(setup_db_required,config.SQLITE_PATH)




##########################################################################
# Create the app and configure it. It is created outside main so that
# it can be imported
##########################################################################
app = create_app()
app.config['sessions'] = dict()

# if setup_db_required:
#     setup.setup_db(app)