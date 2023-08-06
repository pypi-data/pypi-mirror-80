"""
This module will provide configuration management for the PyPayStack framework.
Constant values of the online payment gateway can be registered in a configuration object
which can then be passed to callers or functions
"""
import configparser
import os


__all__ = ('ConfigManager',)

config_filename = 'config.ini'


class Singleton(type):
    # define the singleton behaviour as a meta type
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance


class ConfigManager:
    # create the system configuration manager as singleton
    """
    Support the parsing of application configuration file with attributes that can be
    accessed through get(name) method
    """
    config = None

    def __init__(self, path=None):
        config = configparser.ConfigParser()
        if path and os.path.isfile(path):
            config.read(path)
        else:
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_filename)
            config.read(path)
        self.config = config

    def option(self, section, option):
        if section and option:
            return self.config.get(section, option)

    def configurations(self):
        return self.config.sections()

    @property
    def public_key(self):
        return self.config.get('system', 'public_key')

    @property
    def secret_key(self):
        return self.config.get('system', 'secret_key')

    @property
    def base_url(self):
        return self.config.get('application', 'base-url')

    @property
    def bearer(self):
        return self.config.get('application', 'bearer')

    @property
    def callback_url(self):
        return self.config.get('application', 'callback_url')

    @property
    def currency(self):
        return self.config.get('application', 'currency')

    @property
    def email(self):
        return self.config.get('application', 'email')

    @property
    def per_page(self):
        return self.config.get('application', 'perPage')

    @property
    def transaction_charge(self):
        return self.config.get('application', 'transaction_charge')
