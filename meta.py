import requests
import json


def get_financials(ticker):
    r = requests.get(url='https://api.iextrading.com/1.0/stock/{}/financials'.format(ticker))
    as_dict = json.loads(r.text)
    return as_dict


def get_all_sectors_and_industries(tickers):
    '''
    output as of 3/1/18

    '''

    base_url = 'https://api.iextrading.com/1.0/stock/market/batch?types=company&symbols=s'
    output = {}  # Dict<sector, {set of industries}>

    while tickers:
        batch_size = 100 if len(tickers) >= 100 else len(tickers)

        current_batch = tickers[:batch_size]  # take the first 100
        tickers = tickers[batch_size:]  # trim off the current batch

        batch_as_string = ','.join(current_batch)  # [sq,aapl] -> sq,aapl

        json_data = requests.get(url=base_url + batch_as_string)
        data_as_dict = json.loads(json_data.text)

        for ticker_key in data_as_dict:
            industry = data_as_dict[ticker_key]['company']['industry']
            sector = data_as_dict[ticker_key]['company']['sector']

            # note: industries are part of sectors
            # e.g. SQ: sector = Technology, industry = application software
            if sector not in output:
                output[sector] = {industry}
            else:
                output[sector].add(industry)

    return output


sectors_to_industries = {
    'Basic Materials': {'Chemicals', 'Steel', 'Agriculture', 'Forest Products', 'Coal', 'Metals & Mining',
                        'Building Materials'},

    'Financial Services': {'Insurance', 'Banks', 'Insurance - Life', 'Insurance - Property & Casualty',
                           'Brokers & Exchanges', 'Credit Services', 'Asset Management', 'Insurance - Specialty'},

    'Healthcare': {'Health Care Providers', 'Medical Diagnostics & Research', 'Medical Distribution', 'Biotechnology',
                   'Medical Devices', 'Medical Instruments & Equipment', 'Health Care Plans', 'Drug Manufacturers'},
    '': {''},

    'Industrials': {'Business Services', 'Farm & Construction Machinery', 'Airlines', 'Employment Services',
                    'Waste Management', 'Industrial Distribution', 'Industrial Products', 'Consulting & Outsourcing',
                    'Conglomerates', 'Aerospace & Defense', 'Transportation & Logistics', 'Engineering & Construction',
                    'Truck Manufacturing'},

    'Technology': {'Computer Hardware', 'Application Software', 'Semiconductors', 'Communication Equipment',
                   'Online Media'},

    'Consumer Cyclical': {'Publishing', 'Packaging & Containers', 'Entertainment', 'Personal Services',
                          'Advertising & Marketing Services', 'Restaurants', 'Travel & Leisure',
                          'Homebuilding & Construction', 'Autos', 'Manufacturing - Apparel & Furniture',
                          'Retail - Apparel & Specialty'},

    'Real Estate': {'REITs', 'Real Estate Services'},

    'Energy': {'Oil & Gas - E&P', 'Oil & Gas - Midstream', 'Oil & Gas - Services', 'Oil & Gas - Integrated',
               'Oil & Gas - Drilling', 'Oil & Gas - Refining & Marketing'},

    'Consumer Defensive': {'Tobacco Products', 'Retail - Defensive', 'Education', 'Consumer Packaged Goods',
                           'Beverages - Non-Alcoholic', 'Beverages - Alcoholic'},
    None: {None},

    'Utilities': {'Utilities - Regulated', 'Utilities - Independent Power Producers'},

    'Communication Services': {'Communication Services'}
}
