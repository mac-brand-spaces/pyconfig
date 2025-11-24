from .provider import ConfigProvider
from typing import override

class EnvConfigProvider(ConfigProvider):
  def __init__(self):
    super().__init__()

    from os import environ
    self.environ = environ

  @override
  def _get(self, key):
    transformed_key = self._transform_key(key)
    return self.environ.get(transformed_key)

  def _transform_key(self, key: str) -> str:
    return key.lower().strip().replace(".", "_").upper()
