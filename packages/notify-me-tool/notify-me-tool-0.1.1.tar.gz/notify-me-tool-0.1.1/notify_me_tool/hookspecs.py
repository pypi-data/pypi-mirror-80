import pluggy

hookspec = pluggy.HookspecMarker("notify")


@hookspec
def notify(config: dict):
    """Do whatever you want with your own config values! Send a text, ring a bell,
    whatever your heart desires! The config is meant to store any information
    needed that you don't want to hardcode into your plugin.

    :param config: Configuration for the notification. This will be pulled from
        your config file
    :return: nothing :)
    """
