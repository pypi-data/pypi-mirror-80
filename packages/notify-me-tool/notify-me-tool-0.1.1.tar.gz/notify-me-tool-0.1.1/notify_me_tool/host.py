import configparser
import os
import pluggy

from notify_me_tool import hookspecs, lib
from singleton_decorator import singleton


def main():
    """This is the main entrypoint for notify-me, called by the notify-me command.
    main is responsible for pulling configuration, loading plugins, and running
    them with the config the user passed down.
    """
    config = get_configuration()
    plugin_manager = get_plugin_manager()
    plugin_manager.load_setuptools_entrypoints("notify")

    plugin_manager.hook.notify(config=config)


def get_configuration():
    config = configparser.ConfigParser()
    config.read(get_configuration_file())
    return config


def get_plugin_manager():
    return NotifyMePluginManager().plugin_manager


def get_configuration_file():
    """For now, the configuration file is hard-coded to the ~/.config directory

    :return: path to configuration file
    """
    return os.path.expanduser("~/.config/notify_me/config.ini")


@singleton
class NotifyMePluginManager:
    """
    This class was created so testing was easier. By making this a singleton, we
    can get the same plugin manager as is used in the code so we can register
    test plugins.
    """

    def __init__(self):
        self.plugin_manager = pluggy.PluginManager("notify")
        self.plugin_manager.add_hookspecs(hookspecs)
        self.plugin_manager.register(lib)
