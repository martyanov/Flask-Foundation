from importlib import import_module
from straight.plugin.loaders import ModuleLoader


class AppLoader(ModuleLoader):

    def __init__(self, subtype=None):
        self.subtype = None
        self._cache = []
        super(AppLoader, self).__init__()

    def _fill_cache(self, namespace):
        super(AppLoader, self)._fill_cache(namespace)
        self._cache = filter(self._meta, self._cache)

    def register(self, app):
        for mod in self:
            app.logger.info("Register mod: %s" % mod.__name__)
            self._meta(mod)(app)

    def load_submod(self, submod):
        return filter(
            lambda m: m,
            [self.import_module("%s.%s" % (mod.__name__, submod)) for mod in self]
        )

    def __iter__(self):
        return iter(self._cache)

    @staticmethod
    def _meta(mod):
        return getattr(mod, 'register_app', None)

    @staticmethod
    def import_module(path):
        try:
            return import_module(path)
        except ImportError:
            return None


loader = AppLoader()
loader.load(__name__.split('.')[0])


# pymode:lint_ignore=F0401
