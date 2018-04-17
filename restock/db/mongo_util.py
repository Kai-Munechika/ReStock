from pymongo import MongoClient, ASCENDING, DESCENDING
from restock.config import DB


class DBPoolManager(object):
    """
    Manage database connection, re-using database session
    and create new session when is really needed.
    """
    db_session = None

    def get_connection(self):
        """
        Get new database session

        :return: valid DB session
        :rtype: instance of database client object
        """
        if self.db_session:
            return self.db_session

        self.db_session = MongoClient(DB.URL, maxPoolSize=DB.POOL_SIZE,
                                      serverSelectionTimeoutMS=DB.SELECT_TIMEOUT,
                                      connectTimeoutMS=DB.CONN_TIMEOUT)
        return self.db_session

    def delete_database(self):
        """
        Delete current database *should be used with caution
        """
        try:
            conn = self.get_connection()
            conn.drop_database(DB.DOC)
            print("DATABASE {} DELETED!".format(DB.DOC))
        except Exception as ex:
            raise ex
