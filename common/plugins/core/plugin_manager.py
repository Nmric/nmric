import inspect
import pkgutil
from typing import Dict, List

from .plugin import Plugin


class PluginManager(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    def __init__(self, plugin_repo):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_repo = plugin_repo
        self.reload_plugins()

    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.plugins = []
        self.seen_paths = []
        print()
        print(f'Looking for plugins under package {self.plugin_repo}')
        self.walk_repository(self.plugin_repo)

    def apply_all_plugins_on_value(self, argument):
        """Apply all of the plugins on the argument supplied to this function
        """
        print()
        print(f'Applying all plugins on value {argument}:')
        for plugin in self.plugins:
            print(f'    Applying {plugin.description} on value {argument} yields value {plugin.perform_operation(argument)}')

    def walk_repository(self, package):
        """Recursively walk the supplied package to retrieve all plugins
        """
        imported_package = __import__(package, fromlist=['x'])

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if ispkg:
                plugin_module = __import__(pluginname, fromlist=['_'])
                clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    if issubclass(c, Plugin) & (c is not Plugin):
                        print(f'    Found plugin class: {c.__module__}.{c.__name__}')
                        self.plugins.append(c())

    def get_plugins(self, plugin_type = None) -> Dict[str, Plugin]:
        if plugin_type:
            return {plugin.id: plugin for plugin in self.plugins if isinstance(plugin, plugin_type)}
        
        return self.plugins
        # print(self.plugins)


# plugin_manager = None
# test = None

# def init(pm):
#     global plugin_manager
    
#     if not plugin_manager:
#         print("FIRST PM INIT")
#         plugin_manager = pm

# def initialize():
#     global plugin_manager, test
#     print("INIT")
#     plugin_manager = PluginManager("common.plugins.builtin")
#     print("MANAGER ", plugin_manager)
#     test = 1
