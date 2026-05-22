from os import curdir, path
from typing import cast

_UNSET = cast(None, object())

def find_config_file(name: str, search_dir: str) -> str | None:
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
  return find_config_file(name, parent_dir)
