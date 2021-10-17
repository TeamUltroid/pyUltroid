"""
For multiple database support!
redis cant be remove completely
since, it will be a breaking change
"""


try:
    from deta import Deta
except ImportError:
    Deta = None

class DetaDB:
    def __init__(self, key):
        self.db = Deta(key).Base("Ultroid")

    def set(self, key, value):
        if not self.get(key):
            self.db.insert(value, key)
            return True
        params = {"value":value}
        self.db.update(params, key)
        return True

    def get(self, key, cast=str):
        _get = self.db.get(key)
        if _get:
            return cast(_get["value"])

    def delete(self, key):
        self.db.delete(key)
        return True
