from .provider import ConfigProvider
from .composite_provider import CompositeConfigProvider

_global_composite_provider: CompositeConfigProvider | None = None

def get_global_config_provider() -> CompositeConfigProvider:
  global _global_composite_provider
  if _global_composite_provider is None:
    _global_composite_provider = CompositeConfigProvider([])
  return _global_composite_provider

def add_provider(provider: ConfigProvider) -> None:
  p = get_global_config_provider()
  p.add_provider(provider)

def get_value(key: str, default: str | None = None) -> str:
  return get_global_config_provider().get_value(key, default)

def get_value_int(key: str, default: int | None = None) -> int:
  return get_global_config_provider().get_value_int(key, default)

def get_value_float(key: str, default: int | None = None) -> float:
  return get_global_config_provider().get_value_float(key, default)

def get_value_bool(key: str, default: bool | None = None) -> bool:
  return get_global_config_provider().get_value_bool(key, default)

def get_value_array_str(key: str, default: list[str] | None = None) -> list[str]:
  return get_global_config_provider().get_value_array_str(key, default)


