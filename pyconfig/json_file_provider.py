from .provider import ConfigProvider
from os import curdir, path
from typing import Union, Any


def _find_config_file(name: str, search_dir: str = curdir) -> str | None:
  search_dir = path.abspath(search_dir)
  # Check if the config file exists in the current directory
  config_file = path.join(search_dir, name)
  if path.isfile(config_file):
    rel_path = path.relpath(config_file, curdir)
    return rel_path

  # Check parent directories
  parent_dir = path.dirname(search_dir)
  if parent_dir == search_dir or parent_dir == "": # Reached the root directory
    return None
  return _find_config_file(name, parent_dir)

class JsonFileConfigProvider(ConfigProvider):
  filepath: str

  def __init__(self, filepath: str):
    import json
    self.filepath = filepath
    with open(filepath, "r") as f:
      config = json.load(f)
    self.config = self._flatten(config)

  def _flatten(self, d: dict | Any = None, parent_key: str = "", sep: str = ".") -> dict[str, Any]:
    items: dict[str, Any] = {}
    if not isinstance(d, dict):
      return {parent_key: d} if parent_key else {}
    for k, v in d.items():
      new_key = f"{parent_key}{sep}{k}" if parent_key else k
      if isinstance(v, dict):
        items.update(self._flatten(v, new_key, sep=sep))
      else:
        items[new_key] = v
    return items

  @staticmethod
  def find_config_file(name: str, search_dir: str = curdir) -> Union["JsonFileConfigProvider", None]:
    filepath = _find_config_file(name, search_dir)
    if filepath is None:
      return None
    return JsonFileConfigProvider(filepath)
