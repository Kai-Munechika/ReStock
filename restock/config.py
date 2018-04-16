"""
Configuration file
"""


class DB(object):
    URL = "mongodb://localhost:27017/"
    SELECT_TIMEOUT = 30
    CONN_TIMEOUT = 20000
    POOL_SIZE = 200
    DOC = "ReStocked"
    USERNAME = ""
    PASSWORD = ""


class IEXAPI(object):
    URL = "https://api.iextrading.com/1.0"


class RobinHoodAPI(object):
    URL = "https://api.robinhood.com/fundamentals"
