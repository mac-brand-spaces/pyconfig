from .provider import ConfigProvider, ConfigValue
from typing import Any, Union

type ConfigDict = dict[str, Union[ConfigDict, ConfigValue]]

def flatten(d: Union[ConfigDict, None] = None, parent_key: str = "", sep: str = ".") -> dict[str, Any]:
  items: dict[str, Any] = {}

  if not isinstance(d, dict):
    return {parent_key: d} if parent_key else {}

  for k, v in d.items():
    new_key = k
    if parent_key:
      new_key = f"{parent_key}{sep}{k}"

    if not isinstance(v, dict):
      items[new_key] = v
      continue

    items.update(flatten(v, new_key, sep=sep))

  return items

class DictConfigProvider(ConfigProvider):
  def __init__(self, config: ConfigDict):
    super().__init__()
    self.config = flatten(config)
