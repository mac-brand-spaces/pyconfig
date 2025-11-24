from .provider import ConfigProvider
from typing import Any

class CompositeConfigProvider(ConfigProvider):
  providers: list[ConfigProvider]

  def __init__(self, providers: list[ConfigProvider]):
    super().__init__()

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
