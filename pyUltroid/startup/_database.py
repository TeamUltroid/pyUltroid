import base64
import os

from redis import Redis

from ..configs import Var
from . import LOGS

try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None

try:
    import psycopg2
except ImportError:
    psycopg2 = None
    if Var.DATABASE_URL:
        LOGS.error("'psycopg2' not found!\nInstall psycopg2 to use sql database..")

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


class MongoDB:
    def __init__(self, key):
        self.dB = MongoClient(key, serverSelectionTimeoutMS=5000)
        self.db = self.dB.UltroidDB
        self.re_cache()

    def __repr__(self):
        return f"<Ultroid.MonGoDB\n -total_keys: {len(self.keys())}\n>"

    @property
    def name(self):
        return "Mongo"

    @property
    def usage(self):
        return 0

    def re_cache(self):
        self._cache = {}
        for key in self.keys():
            self._cache.update({key: self.get_key(key)})

    def ping(self):
        if self.dB.server_info():
            return True

    def keys(self):
        return self.db.list_collection_names()

    def set_key(self, key, value):
        if key in self.keys():
            self.db[key].replace_one({"_id": key}, {"value": str(value)})
        else:
            self.db[key].insert_one({"_id": key, "value": str(value)})
        self._cache.update({key: value})
        return True

    def del_key(self, key):
        if key in self.keys():
            try:
                del self._cache[key]
            except KeyError:
                pass
            self.db.drop_collection(key)
            return True

    def get_key(self, key):
        if key in self._cache:
            return self._cache[key]
        if key in self.keys():
            value = self.get(key)
            if value is not None:
                try:
                    value = eval(value)
                except BaseException:
                    pass
                self._cache.update({key: value})
                return value
        return None

    def get(self, key):
        if x := self.db[key].find_one({"_id": key}):
            return x["value"]

    def flushall(self):
        self.dB.drop_database("UltroidDB")
        self._cache = {}
        return True


# --------------------------------------------------------------------------------------------- #

# Thanks to "Akash Pattnaik" / @BLUE-DEVIL1134
# for SQL Implementation in Ultroid.
#
# Please use https://elephantsql.com/ !


class SqlDB:
    def __init__(self, url):
        self._url = url
        self._connection = None
        self._cursor = None
        try:
            self._connection = psycopg2.connect(dsn=url)
            self._connection.autocommit = True
            self._cursor = self._connection.cursor()
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS Ultroid (ultroidCLi varchar(70))"
            )
        except Exception as error:
            LOGS.exception(error)
            LOGS.info("Invaid SQL Database")
            if self._connection:
                self._connection.close()
            sys_exit()

 #   def encrypt(self, data):
#        return base64.b64encode(str(data).encode("utf-8")).decode("utf-8")
#
#    def decrypt(self, data):
#        return base64.b64decode(str(data).encode("utf-8")).decode("utf-8")

    @property
    def name(self):
        return "SQL"

    @property
    def usage(self):
        #        try:
        self._cursor.execute(
            "SELECT pg_size_pretty(pg_relation_size('Ultroid')) AS size"
        )
        data = self._cursor.fetchall()
        return int(data[0][0].split()[0])

    #        except (Exception, psycopg2.DatabaseError) as error:
    #            print("Invaid SQL Database")
    #            if self._connection is not None:
    #                self._connection.close()
    #            sys_exit()
    #            return 0

    def keys(self):
        #        try:
        self._cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name  = 'ultroid'"
        )  # case sensitive
        data = self._cursor.fetchall()
        return data

    #        except (Exception, psycopg2.DatabaseError) as error:
    #            LOGS.info("Invaid SQL Database")
    #            if self._connection is not None:
    #                self._connection.close()
    #            sys_exit()
    #            return False

    def ping(self):
        """They should really keep the `if udB.ping():` in try/except."""
        return True

    get_key = get_data

    def get(self, variable):
        #        try:
        #            try:
        try:
            self._cursor.execute(f"SELECT {variable} FROM Ultroid")
        except psycopg2.errors.UndefinedColumn:
            return None
        data = self._cursor.fetchall()
        if not data:
            return None
        if len(data) >= 1:
            for i in data:
                if i[0]:
                    return i[0]

    #            except (Exception, psycopg2.DatabaseError) as error:
    #                return None
    #        except (Exception, psycopg2.DatabaseError) as error:
    #            if self._connection is not None:
    #                self._connection.close()
    #            sys_exit()
    #            return None

    def set_key(self, key, value):
        #        try:
        try:
            self._cursor.execute(f"ALTER TABLE Ultroid DROP COLUMN {key}")
        except BaseException:
            self._cursor.execute(f"ALTER TABLE Ultroid ADD {key} TEXT")
        self._cursor.execute(
            f"INSERT INTO Ultroid ({key}) values ('{value}')"
        )
        return True

    #        except (Exception, psycopg2.DatabaseError) as error:
    #            print("Invaid SQL Database")
    #            if self._connection is not None:
    #                self._connection.close()
    #            sys_exit()
    #            return False

    def del_key(self, key):
        #        try:
        self._cursor.execute(f"ALTER TABLE Ultroid DROP COLUMN {key}")
        return True

    #        except (Exception, psycopg2.DatabaseError) as error:
    #            print("Invaid SQL Database")
    #            if self._connection is not None:
    #                self._connection.close()
    #            sys_exit()
    #            return True

    def flushall(self):
        #        try:
        self._cursor.execute("DROP TABLE Ultroid")
        self._cursor.execute(
            "CREATE TABLE IF NOT EXISTS Ultroid (ultroidCLi varchar(70))"
        )
        return True

    #       except (Exception, psycopg2.DatabaseError) as error:
    #            print("Invaid SQL Database")
    #            if self._connection is not None:
    #                self._connection.close()
    #            sys_exit()
    #            return False

    def rename(self, key1, key2):
        _ = self.get_key(key1)
        if _:
            self.del_key(key1)
            self.set_key(key2, _)
            return 0
        return 1


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
                import sys

                sys.exit()
        elif not host or not port:
            logger.error("Port Number not found")
            import sys

            sys.exit()
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
        super().__init__(**kwargs)
        self.re_cache()

    # dict is faster than Redis
    def re_cache(self):
        self._cache = {}
        for keys in self.keys():
            self._cache.update({keys: self.get_key(keys)})

    @property
    def name(self):
        return "Redis"

    @property
    def usage(self):
        return sum(self.memory_usage(x) for x in self.keys())

    def set_key(self, key, value):
        value = str(value)
        try:
            value = eval(value)
        except BaseException:
            pass
        self._cache.update({key: value})
        return self.set(str(key), str(value))

    def get_key(self, key):
        if key in self._cache:
            return self._cache[key]
        _ = get_data(self, key)
        self._cache.update({key: _})
        return _

    def del_key(self, key):
        if key in self._cache:
            del self._cache[key]
        return bool(self.delete(str(key)))


# --------------------------------------------------------------------------------------------- #


def UltroidDB():
    if MongoClient and Var.MONGO_URI:
        return MongoDB(Var.MONGO_URI)
    elif psycopg2 and Var.DATABASE_URL:
        return SqlDB(Var.DATABASE_URL)
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
