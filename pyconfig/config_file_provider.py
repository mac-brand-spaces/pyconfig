from .provider import ConfigProvider
from os import curdir
from typing import Union, override
from .util import find_config_file

class ConfigFileConfigProvider(ConfigProvider):
  filepath: str

  def __init__(self, filepath: str):
    super().__init__()
    self.filepath = filepath

    import configparser
    self.config_parser = configparser.ConfigParser(allow_unnamed_section=True)
    self.UNNAMED_SECTION = configparser.UNNAMED_SECTION

    with open(filepath, "r") as f:
      self.config_parser.read_file(f, filepath)

  @override
  def _get(self, key):
    if ('.' in key):
      section, option = key.split('.', 1)
      if self.config_parser.has_section(section):
        s = self.config_parser[section]
        if option in s:
          return s[option]

    s = self.config_parser[self.UNNAMED_SECTION]
    if (key in s):
      return s[key]

    return None

  @staticmethod
  def find_config_file(name: str, search_dir: str = curdir) -> Union["ConfigFileConfigProvider", None]:
    filepath = find_config_file(name, search_dir)
    if filepath is None:
      return None
    return ConfigFileConfigProvider(filepath)
