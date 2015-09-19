
from copy import deepcopy

from twisted.internet import defer
from collections import defaultdict

class Database(object):
    def __init__(self):
        self.content = defaultdict(dict)

    def get(self, key):
        res = deepcopy(self.content[key])
        return defer.succeed(res)

    def write(self, key, value):
        self.content[key] = value
        return defer.succeed(None)

class HasDatabase(object):
    database = Database()
