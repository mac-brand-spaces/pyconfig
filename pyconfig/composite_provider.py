from .provider import ConfigProvider
from typing import Any, override

class CompositeConfigProvider(ConfigProvider):
  providers: list[ConfigProvider]

  def __init__(self, providers: list[ConfigProvider]):
    super().__init__()
    self.providers = providers

  def add_provider(self, provider: ConfigProvider) -> None:
    self.providers.append(provider)

  @override
  def _get(self, key: str) -> Any | None:
    for provider in self.providers:
      value = provider._get(key)
      if value is not None:
        return value
    return None
