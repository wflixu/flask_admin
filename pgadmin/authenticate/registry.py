
"""External Authentication Registry."""


from pgadmin.utils.dynamic_registry import create_registry_metaclass


@classmethod
def load_modules(cls, app=None):
    submodules = []
    from . import internal as module
    submodules.append(module)


    for module in submodules:
        if "init_app" in module.__dict__.keys():
            module.__dict__["init_app"](app)


AuthSourceRegistry = create_registry_metaclass(
    "AuthSourceRegistry", __package__, load_modules=load_modules,
    decorate_as_module=True
)
