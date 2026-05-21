from .dict_provider import DictConfigProvider

class JsonConfigProvider(DictConfigProvider):
  def __init__(self, json_str: str, ignore_json_exception = False):
    import json

    if ignore_json_exception:
      try: config = json.loads(json_str)
      except: config = {}
    else:
      config = json.loads(json_str)

    super().__init__(config)
