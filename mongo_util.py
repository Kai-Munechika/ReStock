from pymongo import MongoClient, DESCENDING
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

#
# def get_top_n_companies_by_metric(n, metric_name, metric_value, sort_metric_name, descending=False):
#     cursor = companies.find({metric_name: metric_value}).sort(sort_metric_name)
#     if descending:
#         cursor = cursor.sort(sort_metric_name, DESCENDING)
#     cursor = cursor.limit(n)
#     return cursor_results_to_list(cursor)


def cursor_results_to_list(cursor):
    """
    :param cursor: pymongo.Cursor
    :return: List[Dictionary]
    """
    result = []
    for doc in cursor:
        result.append(doc)
    return result

