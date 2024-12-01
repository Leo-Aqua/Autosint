import os
import importlib
import inspect
from plugins.plugin_interface import PluginInterface


def load_plugins(plugin_folder: str):
    """
    Dynamically load all valid plugins from the specified folder.
    """
    plugin_instances = {}
    plugin_order = []

    for file in os.listdir(plugin_folder):
        if file.endswith(".py") and file != "plugin_interface.py":
            module_name = file[:-3]
            module = importlib.import_module(f"{plugin_folder}.{module_name}")
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, PluginInterface)
                    and obj is not PluginInterface
                ):
                    instance = obj()
                    key = f"{module_name}.{name}"  # Unique key using the module and class name
                    plugin_instances[key] = {
                        "instance": instance,
                        "active": True,
                    }
                    plugin_order.append(key)

    return plugin_instances, plugin_order
