from typing import Any, Callable
from logging import fatal
from typing import Union
from .util import _UNSET

type ConfigValue = Union[str, int, float, bool, list[Union[str, int, float, bool]]]

class ConfigProvider:
  config: dict[str, ConfigValue]

  def _get(self, key: str) -> Any | None:
    if self.config is None: raise Exception("ConfigProvider base implementation may not be used.")
    return self.config.get(key)

  def _cast_type(self, key: str, value: Any, t: Callable[[Any], Any]) -> Any:
    try:
      return t(value)
    except (ValueError, TypeError):
      fatal("Config value for '%s' is not a valid %s", key, t.__name__)
      exit(1)

  def get_value(self, key: str, default: str | None = _UNSET) -> str:
    config_value = self._get(key)
    if config_value is not None: return self._cast_type(key, config_value, str)

    if default != None: return default
    fatal("Config value for '%s' is not set", key)
    exit(1)

  def get_value_int(self, key: str, default: int | None = _UNSET) -> int:
    config_value = self._get(key)
    if config_value is not None: return self._cast_type(key, config_value, int)

    if default != None: return default
    fatal("Config value for '%s' is not set", key)
    exit(1)

  def get_value_float(self, key: str, default: int | None = _UNSET) -> float:
    config_value = self._get(key)
    if config_value is not None: return self._cast_type(key, config_value, float)

    if default != None: return default
    fatal("Config value for '%s' is not set", key)
    exit(1)

  def get_value_bool(self, key: str, default: bool | None = _UNSET) -> bool:
    config_value = self._get(key)
    if config_value is not None and isinstance(config_value, str): return config_value.lower() in ['1', 'true', 'yes', 'on']
    if config_value is not None: return self._cast_type(key, config_value, bool)

    if default != None: return default
    fatal("Config value for '%s' is not set", key)
    exit(1)

  def get_value_array_str(self, key: str, default: list[str] | None = _UNSET) -> list[str]:
    config_value = self._get(key)
    if config_value is not None and isinstance(config_value, str): return [s.strip() for s in config_value.split(",") if s.strip() != ""]
    if config_value is not None and isinstance(config_value, list): return [self._cast_type(key, v, str) for v in config_value]
    if config_value is not None: return self._cast_type(key, config_value, list)

    if default != None: return default
    fatal("Config value for '%s' is not set", key)
    exit(1)
