import json
from abc import ABC


class BaseModel(ABC):

    def reload(self, items: dict):
        if items is not None:
            self.__dict__ = {k: items.get(k, v) for k, v in self.__dict__.items()}
        return self

    def serialize(self, pretty=True) -> str:
        return json.dumps(self,
                          default=lambda o: {p: getattr(o, p) for p in dir(o.__class__) if
                                             isinstance(getattr(o.__class__, p), property)},
                          indent=2 if pretty else None)

    def to_property_dict(self):
        return json.loads(self.serialize(pretty=False))
