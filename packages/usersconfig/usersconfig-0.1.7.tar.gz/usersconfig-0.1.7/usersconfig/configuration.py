'''
    Configuration reader and parser
'''

# class Config:
#     def __init__(self, **entries):
#         self.__dict__.update(entries)

class Configuration:
    def __init__(self, app_name: str):
        super().__init__()

        self.app_name = app_name

        self.config_file_name = "config.yaml"

        if not self.config_exists():
            self.create_config_dir()
            self.create_default_config_file()
        
        #self.content = self.read_config()

    def load(self):
        ''' Loads the configuration. A factory method. '''
        content = self.read_raw_config()
        return content
        #result = self.parse(content)
        #return result

    def config_exists(self):
        ''' Check if there is a user configuration file '''
        import os.path

        config_path = self.get_config_path()
        result = os.path.exists(config_path)
        return result

    def create_default_config_file(self):
        import pkgutil
        template = pkgutil.get_data(__name__, 'default_config.yml')
        
        path = self.get_config_path()
        with open(path, 'wb') as outfile:
            outfile.write(template)

    def create_config_dir(self):
        ''' Creates the folder to contain the configuration file '''
        import os
        # Create the config folder
        dir = self.get_config_dir()
        if not os.path.exists(dir) and not os.path.isdir(dir):
            os.makedirs(dir)

    def read_raw_config(self):
        import yaml

        path = self.get_config_path()
        content = ''
        with open(path, 'r') as stream:
            try:
                content = yaml.safe_load(stream)
                # print(content)
            except yaml.YAMLError as exc:
                print(exc)

        return content

    def get_config_path(self):
        ''' assembles the path to the config file '''
        from os.path import sep

        return self.get_config_dir() + sep + self.config_file_name

    def get_config_dir(self):
        from xdg.BaseDirectory import xdg_config_home
        from os.path import sep

        return xdg_config_home + sep + self.app_name

    # def parse(self, content):
    #     ''' Parse the config file into an object '''
    #     #from collections import namedtuple
    #     #Config = namedtuple('Config', 'a b d')
    #     obj = Config(**content)
    #     return obj

    # def save(self):
    #     import os
    #     import confuse
    #     import yaml

    #     content = self.config.dump()
    #     #content = yaml.dump(self.config)

    #     config_filename = os.path.join(self.config.config_dir(),
    #                                 confuse.CONFIG_FILENAME)
    #     with open(config_filename, 'w') as f:
    #         #yaml.dump(self.config, f)
    #         f.write(content)

    #     return True
