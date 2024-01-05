
import os
import sys
from flask import Blueprint, current_app, url_for
from collections import defaultdict
from operator import attrgetter
from flask_security.utils import get_post_login_redirect, \
    get_post_logout_redirect

from pgadmin.utils.paths import get_storage_directory

from .preferences import Preferences


IS_WIN = (os.name == 'nt')

def env(name):
    if name in os.environ:
        return os.environ[name]
    return None

def fs_short_path(_path):
    return _path



class PgAdminModule(Blueprint):
    """
    Base class for every PgAdmin Module.

    This class defines a set of method and attributes that
    every module should implement.
    """

    def __init__(self, name, import_name, **kwargs):
        kwargs.setdefault('url_prefix', '/' + name)
        kwargs.setdefault('template_folder', 'templates')
        kwargs.setdefault('static_folder', 'static')
        self.submodules = []
        self.parentmodules = []

        super().__init__(name, import_name, **kwargs)

        def create_module_preference():
            # Create preference for each module by default
            if hasattr(self, 'LABEL'):
                self.preference = Preferences(self.name, self.LABEL)
            else:
                self.preference = Preferences(self.name, None)

            self.register_preferences()

        # Create and register the module preference object and preferences for
        # it just before the first request
        self.before_app_first_request(create_module_preference)

    def register_preferences(self):
        # To be implemented by child classes
        pass

    def register(self, app, options):
        """
        Override the default register function to automagically register
        sub-modules at once.
        """

        super().register(app, options)

        for module in self.submodules:
            module.parentmodules.append(self)
            if app.blueprints.get(module.name) is None:
                app.register_blueprint(module)
                app.register_logout_hook(module)

    def get_own_stylesheets(self):
        """
        Returns:
            list: the stylesheets used by this module, not including any
                stylesheet needed by the submodules.
        """
        return []

    def get_own_messages(self):
        """
        Returns:
            dict: the i18n messages used by this module, not including any
                messages needed by the submodules.
        """
        return dict()

    def get_own_menuitems(self):
        """
        Returns:
            dict: the menuitems for this module, not including
                any needed from the submodules.
        """
        return defaultdict(list)

    def get_panels(self):
        """
        Returns:
            list: a list of panel objects to add
        """
        return []

    def get_exposed_url_endpoints(self):
        """
        Returns:
            list: a list of url endpoints exposed to the client.
        """
        return []

    @property
    def stylesheets(self):
        stylesheets = self.get_own_stylesheets()
        for module in self.submodules:
            stylesheets.extend(module.stylesheets)
        return stylesheets

    @property
    def messages(self):
        res = self.get_own_messages()

        for module in self.submodules:
            res.update(module.messages)
        return res

    @property
    def menu_items(self):
        menu_items = self.get_own_menuitems()
        for module in self.submodules:
            for key, value in module.menu_items.items():
                menu_items[key].extend(value)
        menu_items = dict((key, sorted(value, key=attrgetter('priority')))
                          for key, value in menu_items.items())
        return menu_items

    @property
    def exposed_endpoints(self):
        res = self.get_exposed_url_endpoints()

        for module in self.submodules:
            res += module.exposed_endpoints

        return res


def get_safe_post_login_redirect():
    allow_list = [
        url_for('browser.index')
    ]
    if "SCRIPT_NAME" in os.environ and os.environ["SCRIPT_NAME"]:
        allow_list.append(os.environ["SCRIPT_NAME"])

    url = get_post_login_redirect()
    for item in allow_list:
        if url.startswith(item):
            return url

    return url_for('browser.index')

def get_safe_post_logout_redirect():
    allow_list = [
        url_for('security.login')
    ]
    if "SCRIPT_NAME" in os.environ and os.environ["SCRIPT_NAME"]:
        allow_list.append(os.environ["SCRIPT_NAME"])
    url = get_post_logout_redirect()
    for item in allow_list:
        if url.startswith(item):
            return url
    return url_for('security.login')


def get_complete_file_path(file, validate=True):
    """
    Args:
        file: File returned by file manager

    Returns:
         Full path for the file
    """
    if not file:
        return None

    # If desktop mode
    if current_app.PGADMIN_RUNTIME or not current_app.config['SERVER_MODE']:
        return file if os.path.isfile(file) else None

    storage_dir = get_storage_directory()
    if storage_dir:
        file = os.path.join(
            storage_dir,
            file.lstrip('/').lstrip('\\')
        )
        if IS_WIN:
            file = file.replace('\\', '/')
            file = fs_short_path(file)

    if validate:
        return file if os.path.isfile(file) else None
    else:
        return file
