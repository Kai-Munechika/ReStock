import json
from queue import PriorityQueue

import requests
from operator import itemgetter
from pymongo import MongoClient

from restock.config import IEXAPI, DB
from restock.util.robinhood_api import get_pe_and_market_cap

# TODO: need to check legality of using this API,
# note: using let's us rank ~200 more stocks
USE_ROBINHOOD_API = True
DROP_DB = True


# ~/symbols
def get_active_symbols_and_names():
    # returns all companies that are active have an alphanumeric symbol
    # output : Dictionary[symbol : company name]

    json_data = requests.get(url="{}/ref-data/symbols".format(IEXAPI.URL))
    data_as_list_of_dicts = json.loads(json_data.text)

    symbols_dict = {}
    for _dict in data_as_list_of_dicts:
        if _dict['isEnabled'] and _dict['symbol'].isalnum() \
                and _dict['type'] == 'cs':
            symbols_dict[_dict['symbol']] = {'name': _dict['name']}

    return symbols_dict


# ~/quote
def insert_market_caps_and_pe(company_data, minimum_market_cap):
    # input company_data : Dictionary[
    # symbol: Dictionary['name' : company_name]]
    # for each company in company_data:
    #      Dictionary['name' : company_name] -> Dictionary[
    # 'name' : company_name, 'market_cap' : market_cap]
    # Also removes companies that have market cap < minimum_market_cap

    def process_batch(_company_data, data_as_dict, current_batch_symbols_list):
        for company_symbol in current_batch_symbols_list:
            quote_dict = data_as_dict[company_symbol]['quote']
            market_cap = quote_dict['marketCap']
            pe_ratio = quote_dict['peRatio']
            current_price = quote_dict['latestPrice']

            if USE_ROBINHOOD_API and (not pe_ratio or not market_cap):
                print("robinhood call", company_symbol)
                t = get_pe_and_market_cap(company_symbol)
                if t:
                    if not pe_ratio:
                        pe_ratio = t[0]
                    if not market_cap:
                        market_cap = t[1]

            if market_cap and market_cap > minimum_market_cap and pe_ratio \
                    and pe_ratio > 5:
                _company_data[company_symbol]['market_cap'] = market_cap
                _company_data[company_symbol]['pe_ratio'] = pe_ratio
                _company_data[company_symbol]['price'] = current_price
            else:
                del _company_data[company_symbol]

    batch(company_data=company_data, batch_url_type='quote',
          func_for_each_batch=process_batch)


# ~/company
def insert_sectors_and_industries(company_data, sectors_to_exclude,
                                  industries_to_exclude):
    # input company_data : Dictionary[symbol: Dictionary[
    # 'name' : company_name, 'market_cap' : market_cap]]
    # inserts sector and industry for each company in company_data
    # also removes companies that have sector in sectors_to_exclude
    # or industry in industries_to_exclude

    def process_batch(_company_data, data_as_dict, current_batch_symbols_list):
        for company_symbol in current_batch_symbols_list:
            company_dict = data_as_dict[company_symbol]['company']
            industry = company_dict['industry']
            sector = company_dict['sector']
            if sector not in sectors_to_exclude and industry \
                    not in industries_to_exclude:
                _company_data[company_symbol]['sector'] = sector
                _company_data[company_symbol]['industry'] = industry
            else:
                del _company_data[company_symbol]

    batch(company_data=company_data, batch_url_type='company',
          func_for_each_batch=process_batch)


# ~/stats
def insert_ROA(company_data, minimum_percent=0):
    def process_batch(_company_data, data_as_dict, current_batch_symbols_list):
        for company_symbol in current_batch_symbols_list:
            stats_dict = data_as_dict[company_symbol]['stats']
            ROA = stats_dict['returnOnAssets']
            if ROA and ROA > minimum_percent:
                _company_data[company_symbol]['ROA'] = ROA
            else:
                del _company_data[company_symbol]

    batch(company_data=company_data, batch_url_type='stats',
          func_for_each_batch=process_batch)


# Helper function for every time we need to make > 100 API calls
def batch(company_data, batch_url_type, func_for_each_batch):
    base_url = "{}/stock/market/batch?types={}&symbols=".\
        format(IEXAPI.URL, batch_url_type)
    company_symbols_list = list(company_data.keys())

    while company_symbols_list:
        batch_size = 100 if len(company_symbols_list) >= 100 \
            else len(company_symbols_list)

        # take the first 100
        current_batch_symbols_list = company_symbols_list[:batch_size]
        # trim off the current batch
        company_symbols_list = company_symbols_list[batch_size:]

        # [sq,aapl] -> sq,aapl
        comma_separated_symbols = ','.join(current_batch_symbols_list)

        json_data = requests.get(url=base_url + comma_separated_symbols)
        data_as_dict = json.loads(json_data.text)

        func_for_each_batch(company_data, data_as_dict,
                            current_batch_symbols_list)


# at this point, company_data has everything we need to perform the ranking
def rank_stocks(company_data):
    companies = []  # List[Tuple(symbol, ROA, pe)]
    for symbol in company_data.keys():
        companies.append((symbol, company_data[symbol]['ROA'],
                          company_data[symbol]['pe_ratio']))

    # higher the ROA, the better
    ordered_by_roa = sorted(companies, key=itemgetter(1), reverse=True)
    # lower the p/e ratio, the better
    ordered_by_pe = sorted(companies, key=itemgetter(2))

    # TODO: replace print to logging sending to output and saving in
    # file for troubleshooting
    print(ordered_by_roa)
    print(ordered_by_pe)

    # the lower the score, the better - e.g. a company with a score of
    # 2 is better than a company with a score of 500
    scores = {}
    for i in range(len(ordered_by_roa)):
        tup = ordered_by_roa[i]
        company_symbol = tup[0]
        scores[company_symbol] = i

    for i in range(len(ordered_by_pe)):
        tup = ordered_by_pe[i]
        company_symbol = tup[0]
        scores[company_symbol] += i

    ranking = PriorityQueue()
    for company_symbol in scores:
        ranking.put((scores[company_symbol], company_symbol))

    current_rank = 1
    while ranking.qsize() > 0:
        score, company_symbol = ranking.get()
        company_data[company_symbol]['score'] = score
        company_data[company_symbol]['rank'] = current_rank
        current_rank += 1


def get_comprehensive_company_data():
    company_data = get_active_symbols_and_names()

    # TODO: replace print to logging sending to output and saving
    # in file for troubleshooting
    print('Active symbols and names:')
    print('Size = {}'.format(len(company_data)))
    print()

    # filter out companies
    # note: some companies have null sector and/or industry,
    # these are typically foreign securities or mutual funds
    sectors_to_exclude = frozenset({'Financial Services', ''})
    industries_to_exclude = frozenset({''})  # take a look at REITs

    insert_sectors_and_industries(company_data, sectors_to_exclude,
                                  industries_to_exclude)

    print('With sectors and industries, and after removing those with '
          '"financial services" sector and "REITs" industry')
    print('Size = {}'.format(len(company_data)))
    print()

    # insert ROA and filter out companies with low or invalid ROA
    insert_ROA(company_data)
    print('With ROA, after removing those with a null or < x value')
    print('Size = {}'.format(len(company_data)))
    print()

    # filter out companies that have < $50 million market
    # capitalization or < 5 P/E ratio
    minimum = 50_000_000
    insert_market_caps_and_pe(company_data, minimum)

    print('With market caps and after removing those '
          'with < {} and < 5 P/E ratio'.format(minimum))
    print('Size = {}'.format(len(company_data)))
    print()

    # and finally:
    rank_stocks(company_data)
    print(company_data)

    return company_data


def update_db(company_data):
    """
    :param company_data: Dictionary{
    str company_symbol : Dictionary{string metric : value} }
    :return: None
    """
    # TODO: replace print to logging sending to output
    # and saving in file for troubleshooting
    print()
    print(data)

    client = MongoClient(DB.URL,
                         serverSelectionTimeoutMS=DB.SELECT_TIMEOUT,
                         connectTimeoutMS=DB.CONN_TIMEOUT)
    db = client[DB.DOC]
    companies_collection = db.companies

    if DROP_DB:
        companies_collection.drop()

    for company_symbol in company_data:
        data[company_symbol]['_id'] = company_symbol
        companies_collection.update_one(
            {
                '_id': company_symbol
            },
            {
                '$set': data[company_symbol]
                # upsert=True --> if the document does not exist
                # in the collection, add it
            }, upsert=True)


if __name__ == "__main__":
    data = get_comprehensive_company_data()
    update_db(data)
    print("\n--- BATCH COMPLETED ---\n")
