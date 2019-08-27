import json

def read_only_properties(*attrs):
    def class_rebuilder(cls):
        "The class decorator"

        class NewClass(cls):
            "This is the overwritten class"
            def __setattr__(self, name, value):
                if name not in attrs:
                    pass
                elif name not in self.__dict__:
                    pass
                else:
                    raise AttributeError("Can't modify {}".format(name))

                super().__setattr__(name, value)
        return NewClass
    return class_rebuilder

@read_only_properties('api_key', 'sheet_name')
class Config(object):
    """Class opens json configuration file and converts to config object

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self, config_json_file):
        """[summary]

        Arguments:
            config_json {string} -- path to json file containing configuration
        """
        with open(config_json_file) as config_file:
            config = json.load(config_file)

        self.api_key = config["api_key"]
        self.sheet_name = config["sheet_name"]