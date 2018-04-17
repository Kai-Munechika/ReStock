"""
Configuration file
"""

class DB(object):
    #
    #TODO: fix me! set 0.0.0.0 mongodb in /etc/hosts
    # the issue is in docker-compose.yml flask app needs to connect to mongodb and by
    # documentation I found the DB host is the name of container on this case mongodb
    # temporally add 0.0.0.0 mongodb in your /etc/hosts
    #
    # URL_LOCAL = "mongodb://0.0.0.0:27017/"
    URL = "mongodb://mongodb:27017/"
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
