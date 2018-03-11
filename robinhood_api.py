import requests
import json


def get_pe_and_market_cap(symbol):
    try:
        json_data = requests.get(url='https://api.robinhood.com/fundamentals/{}/'.format(symbol))
        data_as_dict = json.loads(json_data.text)
        return float(data_as_dict['pe_ratio']), float(data_as_dict['market_cap'])
    except:
        return None


