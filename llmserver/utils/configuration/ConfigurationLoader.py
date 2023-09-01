from pathlib import Path
from typing import Union, TypeVar

import yaml

from llmserver.utils.Errors import InvalidStateError
from llmserver.utils.logger import warn, error

T = TypeVar("T")


class ConfigurationLoader(object):

    def __init__(self, file_path: Union[str, Path]):
        self.config = None
        self.file = file_path

    def load_config(self):
        try:
            with open(self.file, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError as e:
            warn(self.__class__.__name__, f"Configuration file at '{self.file}' not found, generating a new one")
            self.__create_config()

        return self

    def __create_config(self):
        try:
            with open(self.file, 'w') as f:
                f.write("")
        except PermissionError as e:
            error(self.__class__.__name__, e)
            raise e

    def get_config(self, label: str):
        if self.config is None:
            raise InvalidStateError("Config not loaded!")

        return self.config[label]

    def configure(self, cls: type[T], section: str = None) -> T:

        if self.config is None:
            raise InvalidStateError("Config not loaded!")

        if section is None:
            section = cls.__name__

        return cls(**self.config[section])
