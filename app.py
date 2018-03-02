import requests
import json


def batch(batch_url_type, company_data, func_for_each_batch):
    base_url = 'https://api.iextrading.com/1.0/stock/market/batch?types={}&symbols='.format(batch_url_type)

    company_symbols_list = list(company_data.keys())
    while company_symbols_list:
        batch_size = 100 if len(company_symbols_list) >= 100 else len(company_symbols_list)

        current_symbols_batch_list = company_symbols_list[:batch_size]       # take the first 100
        company_symbols_list = company_symbols_list[batch_size:]             # trim off the current batch

        comma_separated_symbols = ','.join(current_symbols_batch_list)       # [sq,aapl] -> sq,aapl

        json_data = requests.get(url=base_url + comma_separated_symbols)
        data_as_dict = json.loads(json_data.text)

        func_for_each_batch(company_data, data_as_dict, current_symbols_batch_list)


# ~/symbols
def get_active_symbols_and_names():
    # returns all companies that are active have an alphanumeric symbol
    # output : Dictionary[symbol : company name]

    json_data = requests.get(url='https://api.iextrading.com/1.0/ref-data/symbols')
    data_as_list_of_dicts = json.loads(json_data.text)

    symbols_dict = {}
    for _dict in data_as_list_of_dicts:
        if _dict['isEnabled'] and _dict['symbol'].isalnum():
            symbols_dict[_dict['symbol']] = {'name': _dict['name']}

    return symbols_dict


# ~/quote
def insert_market_caps(company_data, minimum_market_cap):
    # input company_data : Dictionary[symbol: Dictionary['name' : company_name]]
    # for each company in company_data:
    #      Dictionary['name' : company_name] -> Dictionary['name' : company_name, 'market_cap' : market_cap]
    # Also removes companies that have market cap < minimum_market_cap

    # Note: with the api call, we can batch at most 100 companies at a time

    base_url = 'https://api.iextrading.com/1.0/stock/market/batch?types=quote&symbols='
    company_symbols_list = list(company_data.keys())

    while company_symbols_list:
        batch_size = 100 if len(company_symbols_list) >= 100 else len(company_symbols_list)

        current_symbols_batch_list = company_symbols_list[:batch_size]       # take the first 100
        company_symbols_list = company_symbols_list[batch_size:]             # trim off the current batch

        comma_separated_symbols = ','.join(current_symbols_batch_list)       # [sq,aapl] -> sq,aapl

        json_data = requests.get(url=base_url + comma_separated_symbols)
        data_as_dict = json.loads(json_data.text)

        for company_symbol in current_symbols_batch_list:
            quote_dict = data_as_dict[company_symbol]['quote']
            market_cap = quote_dict['marketCap']
            if market_cap and market_cap > minimum_market_cap:
                company_data[company_symbol]['market_cap'] = market_cap
            else:
                # remove the company from our list
                del company_data[company_symbol]


# ~/company
def insert_sectors_and_industries(company_data, sectors_to_exclude=frozenset(), industries_to_exclude=frozenset()):
    # input company_data : Dictionary[symbol: Dictionary['name' : company_name, 'market_cap' : market_cap]]
    # for each company in company_data:
    #   Dictionary['name' : company_name, 'market_cap' : market_cap]]
    #     -> Dictionary['name' : company_name, 'market_cap' : market_cap, 'sector' : sector, 'industry' : industry]]
    # also removes companies that have sector in sectors_to_exclude or industry in industries_to_exclude
    base_url = 'https://api.iextrading.com/1.0/stock/market/batch?types=company&symbols='
    company_symbols_list = list(company_data.keys())

    while company_symbols_list:
        batch_size = 100 if len(company_symbols_list) >= 100 else len(company_symbols_list)

        current_symbols_batch_list = company_symbols_list[:batch_size]       # take the first 100
        company_symbols_list = company_symbols_list[batch_size:]             # trim off the current batch

        comma_separated_symbols = ','.join(current_symbols_batch_list)       # [sq,aapl] -> sq,aapl

        json_data = requests.get(url=base_url + comma_separated_symbols)
        data_as_dict = json.loads(json_data.text)

        for company_symbol in current_symbols_batch_list:
            company_dict = data_as_dict[company_symbol]['company']
            industry = company_dict['industry']
            sector = company_dict['sector']
            if sector not in sectors_to_exclude and industry not in industries_to_exclude:
                company_data[company_symbol]['sector'] = sector
                company_data[company_symbol]['industry'] = industry
            else:
                # remove the company from our list
                del company_data[company_symbol]


def refresh_data():
    company_data = get_active_symbols_and_names()

    print('Active symbols and names:')
    print(company_data)
    print('Size = {}'.format(len(company_data)))
    print()

    # filter out companies that have < $50 million market capitalization
    minimum = 50_000_000
    insert_market_caps(company_data, minimum)

    print('With market caps and after removing those with < {}'.format(minimum))
    print(company_data)
    print('Size = {}'.format(len(company_data)))
    print()

    # filter out companies that have 'financial services' for sector
    sectors_to_exclude = frozenset({'Financial Services'})
    insert_sectors_and_industries(company_data, sectors_to_exclude)

    print('With sectors and industries, and after removing those with "financial services" sector')
    print(company_data)
    print('Size = {}'.format(len(company_data)))
    print()


refresh_data()