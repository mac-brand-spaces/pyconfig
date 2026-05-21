from .dict_provider import DictConfigProvider
from os import curdir
from typing import Union
from .util import find_config_file

class JsonFileConfigProvider(DictConfigProvider):
  filepath: str

  def __init__(self, filepath: str, ignore_json_exception = False):
    self.filepath = filepath

    import json
    with open(filepath, "r") as f:
      if ignore_json_exception:
        try: config = json.load(f)
        except: config = {}
      else:
        config = json.load(f)

    super().__init__(config)

  @staticmethod
  def find_config_file(name: str, search_dir: str = curdir, ignore_json_exception = False) -> Union["JsonFileConfigProvider", None]:
    filepath = find_config_file(name, search_dir)
    if filepath is None: return None
    return JsonFileConfigProvider(filepath, ignore_json_exception)
