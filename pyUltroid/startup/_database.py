"""
For multiple database support!
redis cant be remove completely
since, it will be a breaking change
"""

import asyncio
import os

from redis import Redis

from ..configs import Var
from . import LOGS

try:
    from deta import Deta
except ImportError:
    Deta = None
    if Var.DETA_KEY:
        LOGS.error("'deta' not found!\nInstall deta to use deta base..")

if Deta and Var.DETA_KEY:
    try:
        import nest_asyncio

        nest_asyncio.apply()
    except ImportError:
        pass
# --------------------------------------------------------------------------------------------- #


def get_data(self_, key):
    data = self_.get(str(key))
    if data:
        try:
            data = eval(data)
        except BaseException:
            pass
    return data


# --------------------------------------------------------------------------------------------- #


class DetaDB:
    def __init__(self, key):
        try:
            self._cache = {}
            self.db = Deta(key).AsyncBase("Ultroid")
            self.loop = asyncio.get_event_loop()
            for key in self.run(self.db.fetch()).items:
                if key.get("value"):
                    self._cache.update({key["key"]: key["value"]})
        except Exception as er:
            LOGS.exception(er)

    def __getitem__(self, item):
        return self.get(item)

    @property
    def run(self):
        return self.loop.run_until_complete

    @property
    def name(self):
        return "DetaDB"

    def keys(self):
        return [a["key"] for a in self.run(self.db.fetch()).items]

    def set(self, key, value):
        self._cache.update({str(value): str(key)})
        if not self.get(str(key)):
            try:
                self.run(self.db.insert(str(value), str(key)))
                return True
            except BaseException:
                pass
        params = {"value": str(value)}
        self.run(self.db.update(params, str(key)))
        return True

    def get(self, key, cast=str):
        if key in self._cache:
            return self._cache[key]
        _get = self.run(self.db.get(key))
        if _get is not None:
            self._cache.update({key: _get["value"]})
        if _get is not None:
            return cast(_get["value"])

    def delete(self, key):
        if key in self._cache:
            del self._cache[key]
        if not self.get(key):
            return 0
        self.run(self.db.delete(key))
        return True

    def rename(self, key1, key2):
        get_ = self.get(key1)
        self.delete(key1)
        self.set(key2, get_)

    def ping(self):
        """Deta dont have ping endpoint, while Redis have.."""
        return True

    set_key = set
    del_key = delete

    def get_key(self, key):
        return get_data(self, key)


# --------------------------------------------------------------------------------------------- #


class RedisConnection(Redis):
    def __init__(
        self,
        host,
        port,
        password,
        platform=None,
        logger=LOGS,
        *args,
        **kwargs,
    ):
        if host and ":" in host:
            spli_ = host.split(":")
            host = spli_[0]
            port = int(spli_[-1])
            if host.startswith("http"):
                logger.error("Your REDIS_URI should not start with http !")
                exit()
        elif not host or not port:
            logger.error("Port Number not found")
            exit()
        kwargs["host"] = host
        kwargs["password"] = password
        kwargs["port"] = port

        if platform.lower() == "qovery" and not host:
            var, hash_, host, password = "", "", "", ""
            for vars_ in os.environ:
                if vars_.startswith("QOVERY_REDIS_") and vars.endswith("_HOST"):
                    var = vars_
            if var:
                hash_ = var.split("_", maxsplit=2)[1].split("_")[0]
            if hash:
                kwargs["host"] = os.environ(f"QOVERY_REDIS_{hash_}_HOST")
                kwargs["port"] = os.environ(f"QOVERY_REDIS_{hash_}_PORT")
                kwargs["password"] = os.environ(f"QOVERY_REDIS_{hash_}_PASSWORD")
        if logger:
            logger.info("Connecting to redis database")
        super().__init__(**kwargs)
        self.re_cache()

    # dict is faster than Redis
    def re_cache(self):
        self._cache = {}
        for keys in self.keys():
            self._cache.update({keys: self.get_key(keys)})

    def set_key(self, key, value):
        try:
            value = eval(value)
        except BaseException:
            pass
        if isinstance(value, list) or isinstance(value, dict):
            del self._cache[key]
        self._cache.update({key: value})
        return self.set(str(key), str(value))

    def get_key(self, key):
        if key in self._cache:
            return self._cache[key]
        return get_data(self, key)

    def del_key(self, key):
        if key in self._cache:
            del self._cache[key]
        return bool(self.delete(str(key)))

    @property
    def name(self):
        return "Redis"


# --------------------------------------------------------------------------------------------- #


def UltroidDB():
    if Deta and Var.DETA_KEY:
        return DetaDB(Var.DETA_KEY)
    from .. import HOSTED_ON

    return RedisConnection(
        host=Var.REDIS_URI or Var.REDISHOST,
        password=Var.REDIS_PASSWORD or Var.REDISPASSWORD,
        port=Var.REDISPORT,
        platform=HOSTED_ON,
        decode_responses=True,
        socket_timeout=5,
        retry_on_timeout=True,
    )


# --------------------------------------------------------------------------------------------- #
