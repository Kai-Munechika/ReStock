import pytest
from pymongo import MongoClient
from restock.db.mongo_util import DBPoolManager

"""
how to run: 

 1. initialize python virutal env with command: make init
 2. load python virtual env: source venv/bin/active
 3. run tests: pytest -s tests/db/test_db_pool_manager.py
"""

class TestDBPoolManager(object):
    """
    Test Database Pool Manager
    :Tests:
        - test_get_connection
    """

    db_pool = DBPoolManager()

    def test_get_connection(self):
        """Test DB connectivity"""
        conn = self.db_pool.get_connection()
        # The ismaster command is cheap and does not require auth.
        conn.admin.command('ismaster')
        assert(conn)
        info = conn.server_info()
        assert(info)
        print(info)
