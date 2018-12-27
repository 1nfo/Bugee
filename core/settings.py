import configparser
from functools import partial

from os.path import dirname, abspath, join

abs_path = partial(join, dirname(abspath(__file__)))

__all__ = ['settings']


class _Settings:
    SETTING_FILE = "config.ini"
    DB_SECTION = "database"
    FLASK_SECTION = 'flask'

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read(abs_path(self.SETTING_FILE))

    @property
    def config(self) -> configparser.ConfigParser:
        return self._config

    def show_all(self):
        for key in self.config.keys():
            for k, v in self.config[key].items():
                print(k, v)

    @property
    def db_setting(self):
        return self.config[_Settings.DB_SECTION]

    @property
    def flask_setting(self):
        return self.config[_Settings.FLASK_SECTION]


settings = _Settings()
