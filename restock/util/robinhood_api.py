import json
import requests
from restock.config import RobinHoodAPI


def get_pe_and_market_cap(symbol):
    try:
        json_data = requests.get(url='{}/{}/'.format(RobinHoodAPI.URL, symbol))
        data_as_dict = json.loads(json_data.text)
        return float(data_as_dict['pe_ratio']), float(data_as_dict['market_cap'])
    except:
        return None
