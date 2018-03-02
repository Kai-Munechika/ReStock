import requests
import json


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

    def process_batch(_company_data, data_as_dict, current_batch_symbols_list):
        for company_symbol in current_batch_symbols_list:
            quote_dict = data_as_dict[company_symbol]['quote']
            market_cap = quote_dict['marketCap']
            if market_cap and market_cap > minimum_market_cap:
                _company_data[company_symbol]['market_cap'] = market_cap
            else:
                del _company_data[company_symbol]

    batch(company_data=company_data, batch_url_type='quote', func_for_each_batch=process_batch)


# ~/company
def insert_sectors_and_industries(company_data, sectors_to_exclude, industries_to_exclude):
    # input company_data : Dictionary[symbol: Dictionary['name' : company_name, 'market_cap' : market_cap]]
    # inserts sector and industry for each company in company_data
    # also removes companies that have sector in sectors_to_exclude or industry in industries_to_exclude

    def process_batch(_company_data, data_as_dict, current_batch_symbols_list):
        for company_symbol in current_batch_symbols_list:
            company_dict = data_as_dict[company_symbol]['company']
            industry = company_dict['industry']
            sector = company_dict['sector']
            if sector not in sectors_to_exclude and industry not in industries_to_exclude:
                _company_data[company_symbol]['sector'] = sector
                _company_data[company_symbol]['industry'] = industry
            else:
                del _company_data[company_symbol]

    batch(company_data=company_data, batch_url_type='company', func_for_each_batch=process_batch)


# todo
# ~/financials
def insert_financials(company_data):
    # inserts ROC, Earnings Yield, EBIT, totalAssets, totalDebt, and currentCash for each company in company data

    def process_batch(_company_data, data_as_dict, current_batch_symbols_list):
        for company_symbol in current_batch_symbols_list:
            

    batch(company_data=company_data, batch_url_type='financials', func_for_each_batch=process_batch)


# Helper function for every time we need to make > 100 API calls
def batch(company_data, batch_url_type, func_for_each_batch):
    base_url = 'https://api.iextrading.com/1.0/stock/market/batch?types={}&symbols='.format(batch_url_type)
    company_symbols_list = list(company_data.keys())

    while company_symbols_list:
        batch_size = 100 if len(company_symbols_list) >= 100 else len(company_symbols_list)

        current_batch_symbols_list = company_symbols_list[:batch_size]       # take the first 100
        company_symbols_list = company_symbols_list[batch_size:]             # trim off the current batch

        comma_separated_symbols = ','.join(current_batch_symbols_list)       # [sq,aapl] -> sq,aapl

        json_data = requests.get(url=base_url + comma_separated_symbols)
        data_as_dict = json.loads(json_data.text)

        func_for_each_batch(company_data, data_as_dict, current_batch_symbols_list)


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

    # # filter out companies that have 'financial services' for sector
    # note: some companies have null sector and/or industry, these are typically foreign securities or mutual funds
    sectors_to_exclude = frozenset({'Financial Services', ''})
    industries_to_exclude = frozenset({''})

    insert_sectors_and_industries(company_data, sectors_to_exclude, industries_to_exclude)

    print('With sectors and industries, and after removing those with "financial services" sector')
    print(company_data)
    print('Size = {}'.format(len(company_data)))
    print()


refresh_data()