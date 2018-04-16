from src.config import DB
from src.db.mongo_util import DBPoolManager


class Companies(object):
    """
    ReStocked Company(ies) Entity
    """

    db_pool = DBPoolManager()
    conn = db_pool.get_connection()
    entity = conn[DB.DOC]
    companies = entity.companies

    def cursor_results_to_list(self, cursor):
        """
        :param cursor: pymongo.Cursor
        :return: List[Dictionary]
        """
        result = []
        for doc in cursor:
            result.append(doc)
        return result

    def get_company(self, symbol=None):
        """
        :param symbol: String
        :return: (dict) contains Company
        """
        if symbol:
            return self.companies.find_one({'_id': symbol})

        return self.companies.find()

        # TODO: Can these lines below be deleted?
        # return companies.find({'rank' : {'$lt': n}}, {'name': 0}).sort('rank')
        # return companies.find({'rank': {'$lt': n}}, {'_id':1, 'rank':1}).sort('rank')

    def drop_companies(self):
        """
        Delete Companies doc in the database
        """
        self.companies.drop()

    def get_top_n_ranked_companies(self, n):
        """
        Get top ranked companies from database
        :param n: int   #TODO: parameters need better names
        :return: list of dict
        """
        cursor = self.companies.find({'rank': {'$lte': n}}).sort('rank')
        return self.cursor_results_to_list(cursor)

    def get_top_n_companies_filtered(self, n, filter_attribute, filter_value,
                                     sort_attribute, order=None):
        """
        We want to filter the companies by some discrete attribute/metric: e.g. industry,
        sector and want to sort the results by some numerical
        value: e.g. ROA, P/E ratio, or rank, descending or ascending

        :param filter_attribute:
        :type filter_attribute:
        :param filter_value:
        :type filter_value:
        :param sort_attribute:
        :type sort_attribute:
        :param order:
        :type order:
        :return:
        :rtype:
        """

        if not order:
            order = "ASCENDING"

        cursor = self.companies.find({filter_attribute: filter_value}).sort(sort_attribute, order).limit(n)
        return self.cursor_results_to_list(cursor)
