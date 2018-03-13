from pymongo import MongoClient, ASCENDING, DESCENDING
client = MongoClient()
db = client['ReStocked']
companies = db.companies


# return companies.find({'rank' : {'$lt': n}}, {'name': 0}).sort('rank')
# return companies.find({'rank': {'$lt': n}}, {'_id':1, 'rank':1}).sort('rank')


def get_company(symbol):
    """
    :param symbol: String
    :return: Dictionary
    """
    return companies.find_one({'_id': symbol})


def drop_companies():
    companies.drop()


def get_top_n_ranked_companies(n):
    """
    :param n: int
    :return: List[Dictionary]
    """
    cursor = companies.find({'rank': {'$lte': n}}).sort('rank')
    return cursor_results_to_list(cursor)


# We want to filter the companies by some discrete attribute/metric: e.g. industry, sector
# and want to sort the results by some numerical value: e.g. ROA, P/E ratio, or rank, descending or ascending
def get_top_n_companies_filtered(n, filter_attribute, filter_value, sort_attribute, order=ASCENDING):
    cursor = companies.find({filter_attribute: filter_value}).sort(sort_attribute, order).limit(n)
    return cursor_results_to_list(cursor)


def cursor_results_to_list(cursor):
    """
    :param cursor: pymongo.Cursor
    :return: List[Dictionary]
    """
    result = []
    for doc in cursor:
        result.append(doc)
    return result

