from os import environ, curdir, path
from typing import Any, Callable
from logging import fatal

class ConfigProvider:
  config: dict[str, Any] = {}

  def _get(self, key: str) -> Any | None:
    return self.config.get(key)

  def _cast_type(self, key: str, value: Any, t: Callable[[Any], Any]) -> Any:
    try:
      return t(value)
    except (ValueError, TypeError):
      fatal("Config value for '%s' is not a valid %s", key, t.__name__)
      exit(1)

  def get_value(self, key: str, default: str | None = None) -> str:
    config_value = self._get(key)
    if config_value is not None: return self._cast_type(key, config_value, str)

    if default is not None: return default
    fatal("Config value for '%s' is not set", key)
    exit(1)

  def get_value_int(self, key: str, default: int | None = None) -> int:
    config_value = self._get(key)
    if config_value is not None: return self._cast_type(key, config_value, int)

    if default is not None: return default
    fatal("Config value for '%s' is not set", key)
    exit(1)

  def get_value_bool(self, key: str, default: bool | None = None) -> bool:
    config_value = self._get(key)
    if config_value is not None and isinstance(config_value, str): return config_value.lower() in ['1', 'true', 'yes', 'on']
    if config_value is not None: return self._cast_type(key, config_value, bool)

    if default is not None: return default
    fatal("Config value for '%s' is not set", key)
    exit(1)

  def get_value_array_str(self, key: str, default: list[str] | None = None) -> list[str]:
    config_value = self._get(key)
    if config_value is not None and isinstance(config_value, str): return [s.strip() for s in config_value.split(",") if s.strip() != ""]
    if config_value is not None and isinstance(config_value, list): return [self._cast_type(key, v, str) for v in config_value]
    if config_value is not None: return self._cast_type(key, config_value, list)

    if default is not None: return default
    fatal("Config value for '%s' is not set", key)
    exit(1)

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
  def find_config_file(name: str, search_dir: str = curdir) -> JsonFileConfigProvider | None:
    filepath = _find_config_file(name, search_dir)
    if filepath is None:
      return None
    return JsonFileConfigProvider(filepath)

class EnvConfigProvider(ConfigProvider):
  def __init__(self):
    for key, value in environ.items():
      transformed_key = self._transform_key(key)
      self.config[transformed_key] = value

  def _transform_key(self, key: str) -> str:
    return key.lower().strip().replace(".", "_").upper()

class CompositeConfigProvider(ConfigProvider):
  providers: list[ConfigProvider]

  def __init__(self, providers: list[ConfigProvider]):
    self.providers = providers
    self.config = self._merge_configs()

  def add_provider(self, provider: ConfigProvider) -> None:
    self.providers.append(provider)
    self.config = self._merge_configs()

  def _merge_configs(self) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for provider in reversed(self.providers):
      merged.update(provider.config)
    return merged
