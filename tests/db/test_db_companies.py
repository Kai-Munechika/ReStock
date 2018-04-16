import pytest
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from src.config import DB
from src.controller.Company import Companies

"""
how to run: 

 1. initialize python virutal env with command: make init
 2. load python virtual env: source venv/bin/active
 3. run tests: pytest -s tests/db/test_db_companies.py
"""

class TestDBCompanies(object):
    """
    Test Companies database Entity using DB Pool Manager

    :Tests:
        - test_db_get_companies
        - test_db_get_company_by_stock_symbol
    """

    companies = Companies()

    def test_get_companies(self):
        """Test Companies document exists and has more than 2k records"""
        assert(self.companies.get_company())
        assert(self.companies.get_company().count() > 2000)


    def test_db_get_company_by_stock_symbol(self):
        """Test Companies document saved into database by stock symbol"""
        assert(len(self.companies.get_company(symbol="RHT")) > 0)
        assert("Red Hat" in self.companies.get_company(symbol="RHT")["name"])
        assert ("Application Software" in self.companies.get_company(symbol="RHT")["industry"])
