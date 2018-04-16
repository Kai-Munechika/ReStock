import pytest
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from src.config import DB

"""
how to run: 

 1. initialize python virutal env with command: make init
 2. load python virtual env: source venv/bin/active
 3. run tests: pytest -s tests/db/test_db.py
"""

class TestDB(object):
    """
    Test MongoDB using classic DB connection without Pool manager

    :Tests:
        - test_test_db_connection
        - test_db_get_companies
        - test_db_get_company_by_stock_symbol
    """

    def test_db_connection(self):
        """Test DB connectivity"""
        client = MongoClient(DB.URL,
                             serverSelectionTimeoutMS=DB.SELECT_TIMEOUT,
                             connectTimeoutMS=DB.CONN_TIMEOUT)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        assert(client)
        info = client.server_info()
        assert(info)
        print(info)

    def test_db_get_companies(self):
        """Get companies record from ReStocked DOC"""
        client = MongoClient(DB.URL,
                             serverSelectionTimeoutMS=DB.SELECT_TIMEOUT,
                             connectTimeoutMS=DB.CONN_TIMEOUT)
        db = client[DB.DOC]
        assert "companies" in db.collection_names()
        companies = db.companies
        assert(companies.find({}).count() > 0)

    def test_db_get_company_by_stock_symbol(self, symbol="RHT"):
        """Get company info by stock symbol"""
        client = MongoClient(DB.URL,
                             serverSelectionTimeoutMS=DB.SELECT_TIMEOUT,
                             connectTimeoutMS=DB.CONN_TIMEOUT)
        db = client[DB.DOC]
        companies = db.companies
        redhat = list(companies.find({"_id":"RHT"}))
        assert len(redhat) > 0
        assert "Red Hat" in redhat[0]['name']
