import yaml
import os


class cfg:
    config = {}

    @classmethod
    def get_config(cls):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        cls.config = yaml.load(open("botconfigs.yml", "r"), yaml.CLoader)
        return cls.config

    @classmethod
    def export_config(cls):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        yaml.dump(cls.config, open("botconfigs.yml", 'w'), yaml.CDumper)
